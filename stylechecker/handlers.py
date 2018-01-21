import io
import os
import random

from django.conf import settings
from packtools.utils import config_xml_catalog
from packtools import stylechecker


def _create_error_menu(xml_validator):
    summary = stylechecker.summarize(xml_validator)
    menu = []
    for item in summary['dtd_errors']:
        menu.append(item)

    style_errors_menu = {}
    for key, errors in sorted(summary['style_errors'].items()):
        for error in errors:
            if style_errors_menu.get(error['message']):
                style_errors_menu[error['message']].append(
                    error['apparent_line']
                )
            else:
                style_errors_menu[error['message']] = [error['apparent_line']]
    menu.append(style_errors_menu)
    return menu


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
        with open(result_xml_name, 'w+b') as fb:
            stylechecker.annotate(xml_validator, fb)
        menu = _create_error_menu(xml_validator)
        return is_valid, menu, result_xml_name
