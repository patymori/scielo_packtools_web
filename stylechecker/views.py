from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import UploadXMLFileForm


def home(request):
    return render(request, "index.html", {})


class XMLValidateView(FormView):
    form_class = UploadXMLFileForm
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        form = UploadXMLFileForm(request.POST, request.FILES)
        if form.is_valid():
            return reverse('stylechecker:xml-validator')
