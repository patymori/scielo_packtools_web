from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import UploadXMLFileForm
from .handlers import validate_xml_handler


class XMLValidateView(FormView):
    form_class = UploadXMLFileForm
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        form = UploadXMLFileForm(request.POST, request.FILES)
        if form.is_valid():
            is_valid, menu, result_name_file = validate_xml_handler(
                request.FILES['file']
            )
            context = {
                'form': form,
                'menu': menu if not is_valid else []
            }
            if not is_valid:
                result = open(result_name_file, 'r').read()
                context.update({
                   'xmlfile': result
                })

            return render(
                request,
                context=context,
                template_name=self.template_name
            )
