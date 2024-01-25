from django.views.generic import FormView
from .forms import TypographieFilterForm


class TypographieFilter(FormView):
    template_name = "typographie/typographie.html"
    form_class = TypographieFilterForm

    def form_valid(self, form):
        filtered_text = form.filter()
        form = self.form_class(initial={"text_to_filter": filtered_text})
        return self.render_to_response(self.get_context_data(form=form))
