from functools import update_wrapper

from django.contrib.admin.utils import unquote
from django.contrib import admin
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db import models
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from typographie.typographie import typographie


def apply_typographie_to_dict(d, fields):
    new_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            new_dict[k] = apply_typographie_to_dict(v, fields)
        elif isinstance(v, list):
            new_dict[k] = []
            for i in v:
                new_dict[k].append(apply_typographie_to_dict(i, fields))
        else:
            if k in fields:
                v = typographie(v)
            new_dict[k] = v
    return new_dict


def apply_typographie(obj):
    for field_name in obj.typographie_fields:
        try:
            field = getattr(obj, field_name)
        except ObjectDoesNotExist:
            continue

        if isinstance(field, str):
            setattr(obj, field_name, typographie(field))

        # This is probably a JSONField
        elif isinstance(field, dict):
            try:
                fields = getattr(obj, f"get_typographie_{field_name}_fields")()
            except AttributeError:
                continue
            setattr(obj, field_name, apply_typographie_to_dict(field, fields))

        # Is it a FK, a OneToOne or reversed OneToOne
        elif issubclass(field.__class__, models.Model):
            apply_typographie(field)

        # Is it a M2M or a reversed M2M
        elif issubclass(field.__class__, models.Manager):
            for related in field.all():
                apply_typographie(related)

    obj.save()


class TypographieAdmin(admin.ModelAdmin):
    def _info(self):
        return {
            "app_label": self.model._meta.app_label,
            "model_name": self.model._meta.model_name,
        }

    def get_urls(self):
        from django.conf.urls import url

        urlpatterns = super().get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        typo_url = [
            url(
                r"^(.+)/typo/$",
                wrap(self.typo_view),
                name="{app_label}_{model_name}_typo".format(**self._info()),
            )
        ]

        return typo_url + urlpatterns

    def typo_view(self, request, object_id, extra_contexte=None):
        obj = get_object_or_404(self.get_queryset(request), pk=unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        apply_typographie(obj)

        return redirect(
            reverse(
                "admin:{app_label}_{model_name}_change".format(**self._info()), args=(object_id,)
            )
        )
