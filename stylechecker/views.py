from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import UploadXMLFileForm
from .models import XMLFileValidator


class XMLValidateView(FormView):
    form_class = UploadXMLFileForm
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        form = UploadXMLFileForm(request.POST, request.FILES)
        if form.is_valid():
            context = {'form': form}
            xml_file_validator = XMLFileValidator(request.FILES['file'])
            if not xml_file_validator.validate_handler():
                classified_errors = xml_file_validator.classify_errors()
                context.update({'summary': classified_errors})
            return render(
                request,
                context=context,
                template_name=self.template_name
            )
