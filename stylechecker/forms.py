from django import forms


class UploadXMLFileForm(forms.Form):
    file = forms.FileField(allow_empty_file=False)
