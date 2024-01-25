from django import forms
from tinymce.widgets import TinyMCE
from typographie.admin import typographie


class TypographieFilterForm(forms.Form):
    class Media:
        js = ("/static/tinymce/tinymce.min.js",)

    text_to_filter = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "initial" in kwargs:
            self.fields["text_to_filter"].initial = kwargs["initial"].get(
                "text_to_filter", ""
            )

    def filter(self):
        text_value = self.cleaned_data.get("text_to_filter", "")
        return typographie(text_value)
