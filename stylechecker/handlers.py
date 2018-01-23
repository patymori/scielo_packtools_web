import os

from django.conf import settings
from packtools.utils import config_xml_catalog
from packtools import stylechecker


def _parse_sps_error_detail(xml_result, error_line):
    start_line = error_line - 3 if error_line >= 3 else 0
    end_line = -1 if error_line >= len(xml_result) else error_line + 3
    xml_result_lines = xml_result[start_line:end_line]
    return {
        'apparent_line': error_line,
        'doc_slice': ''.join(xml_result_lines)
    }


def _create_sps_errors_object(xml_result, errors):
    style_errors_menu = {
        error['message']: [
            _parse_sps_error_detail(xml_result, index)
            for index, line in enumerate(xml_result)
            if error['message'] in line
        ]
        for error in errors
    }
    import pdb; pdb.set_trace()
    return style_errors_menu


def _create_error_menu(result_xml_name, xml_validator):
    summary = stylechecker.summarize(xml_validator)
    menu = []
    for item in summary['dtd_errors']:
        menu.append(item)

    xml_result = None
    with open(result_xml_name, 'r') as xml:
        xml_result = [line for line in xml]

    for _, errors in sorted(summary['style_errors'].items()):
        style_errors_menu = _create_sps_errors_object(xml_result, errors)
    menu.append(style_errors_menu)
    return menu


def _generate_html_result(filename, xml_validator):
    result_xml_name = os.path.join(
        settings.MEDIA_ROOT,
        'result_{}'.format(filename)
    )
    with open(result_xml_name, 'w+b') as fb:
        stylechecker.annotate(xml_validator, fb)

    return result_xml_name


@config_xml_catalog
def validate_xml_handler(uploadedFile):
    xml_validator = stylechecker.get_xmlvalidator(
        xmlpath=uploadedFile,
        no_network=True,
        extra_sch=[]
    )
    is_valid, _ = xml_validator.validate_all()
    if is_valid:
        return is_valid
    else:
        result_xml_name = _generate_html_result(uploadedFile.name,
                                                xml_validator)
        menu = _create_error_menu(result_xml_name, xml_validator)
        return is_valid, menu, result_xml_name
