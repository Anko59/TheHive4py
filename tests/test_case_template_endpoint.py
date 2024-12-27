from typing import List

import pytest
from thehive4py.client import TheHiveApi
from thehive4py.errors import TheHiveError
from thehive4py.types.case_template import InputCaseTemplate, OutputCaseTemplate


class TestCaseTemplateEndpoint:
    def test_create_and_get(self, thehive: TheHiveApi):
        created_case_template = thehive.case_template.create(
            case_template={
                "name": "my first template",
                "description": "Template description",
            }
        )
        fetched_case_template = thehive.case_template.get(created_case_template["_id"])
        assert created_case_template == fetched_case_template

    def test_update(self, thehive: TheHiveApi, test_case_template: OutputCaseTemplate):
        case_template_id = test_case_template["_id"]
        update_fields: InputCaseTemplate = {
            "name": "updated template name",
            "description": "updated template description",
        }
        thehive.case_template.update(
            case_template_id=case_template_id, fields=update_fields
        )
        updated_case_template = thehive.case_template.get(
            case_template_id=case_template_id
        )

        for key, value in update_fields.items():
            assert updated_case_template.get(key) == value

    def test_update_with_wrong_argument_error(
        self, thehive: TheHiveApi, test_case_template: OutputCaseTemplate
    ):
        case_template_id = test_case_template["_id"]
        update_fields: InputCaseTemplate = {
            "name": "updated template name",
            "description": "updated template description",
        }
        wrong_kwargs = {"template_fields": update_fields, "wrong_arg": "value"}
        with pytest.raises(TheHiveError, match=rf".*{list(wrong_kwargs.keys())}.*"):
            thehive.case_template.update(case_template_id=case_template_id, **wrong_kwargs)  # type: ignore

    def test_delete(self, thehive: TheHiveApi, test_case_template: OutputCaseTemplate):
        case_template_id = test_case_template["_id"]
        thehive.case_template.delete(case_template_id=case_template_id)
        with pytest.raises(TheHiveError):
            thehive.case_template.get(case_template_id=case_template_id)

    def test_find(
        self,
        thehive: TheHiveApi,
        test_case_templates: List[OutputCaseTemplate],
    ):
        filters = {"name": "my first template"}
        found_templates = thehive.case_template.find(filters=filters)
        names = [template["name"] for template in found_templates]
        for test_template in test_case_templates:
            assert test_template["name"] in names