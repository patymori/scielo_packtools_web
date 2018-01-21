import io
import os
import random

from django.conf import settings
from packtools.utils import config_xml_catalog
from packtools import stylechecker


@config_xml_catalog
def validate_xml_handler(uploadedFile):
    result_xml_name = os.path.join(
        settings.MEDIA_ROOT,
        'result_{}'.format(uploadedFile.name)
    )

    xml_validator = stylechecker.get_xmlvalidator(
        xmlpath=uploadedFile,
        no_network=True,
        extra_sch=[]
    )
    is_valid, _ = xml_validator.validate_all()
    if is_valid:
        return is_valid
    else:
        import pdb; pdb.set_trace()
        with open(result_xml_name, 'w+b') as fb:
            stylechecker.annotate(xml_validator, fb)
        summary = stylechecker.summarize(xml_validator)
        return is_valid, summary, result_xml_name
