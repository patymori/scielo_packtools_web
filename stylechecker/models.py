import os

from django.db import models
from django.conf import settings
from packtools.utils import config_xml_catalog
from packtools import stylechecker


class XMLFileValidator:

    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def _generate_html_result(self):
        self.result_xml_name = os.path.join(
            settings.MEDIA_ROOT,
            'result_{}'.format(self.uploaded_file.name)
        )
        with open(self.result_xml_name, 'w+b') as fb:
            stylechecker.annotate(self.xml_validator, fb)

    def _create_sps_errors_object(self, xml_result, errors):
        style_errors_object = [{
            error['message']: [
                self._parse_sps_error_detail(xml_result, index)
                for index, line in enumerate(xml_result)
                if error['message'] in line
            ]
            for error in errors
        }]
        return style_errors_object

    def _parse_sps_error_detail(self, xml_result, error_line):
        start_line = error_line - 3 if error_line >= 3 else 0
        end_line = -1 if error_line >= len(xml_result) else error_line + 3
        xml_result_lines = xml_result[start_line:end_line]
        return {
            'apparent_line': error_line,
            'doc_slice': ''.join(xml_result_lines)
        }

    def classify_errors(self):
        summary = stylechecker.summarize(self.xml_validator)
        classified_errors = {
            'dtd_errors': [item for item in summary['dtd_errors']]
        } if summary['dtd_errors'] else {}

        self._generate_html_result()
        xml_result = None
        with open(self.result_xml_name, 'r') as xml:
            xml_result = [line for line in xml]

        classified_errors.update({
            'style_errors': self._create_sps_errors_object(xml_result, errors)
            for _, errors in summary['style_errors'].items()
        })
        return classified_errors

    @config_xml_catalog
    def validate_handler(self):
        self.xml_validator = stylechecker.get_xmlvalidator(
            xmlpath=self.uploaded_file,
            no_network=True,
            extra_sch=[]
        )
        is_valid, _ = self.xml_validator.validate_all()
        return is_valid
