import libcst as cst
from core_codemods.api import (
    Metadata,
    Reference,
    ReviewGuidance,
    SimpleCodemod,
)


class DjangoJsonResponseType(SimpleCodemod):
    metadata = Metadata(
        name="django-json-response-type",
        summary="Set content type to `application/json` for `django.http.HttpResponse` with JSON data",
        review_guidance=ReviewGuidance.MERGE_WITHOUT_REVIEW,
        references=[
            Reference(
                url="https://docs.djangoproject.com/en/4.0/ref/request-response/#django.http.HttpResponse.__init__"
            ),
            Reference(
                url="https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#output-encoding-for-javascript-contexts"
            ),
        ],
    )
    change_description = "Sets `content_type` to `application/json`."
    detector_pattern = """
        rules:
          - id: django-json-response-type
            mode: taint
            pattern-sources:
              - pattern: json.dumps(...)
            pattern-sinks:
              - patterns:
                - pattern: django.http.HttpResponse(...)
                - pattern-not: django.http.HttpResponse(...,content_type=...,...)
        """

    def on_result_found(self, _, updated_node):
        return self.update_arg_target(
            updated_node,
            [
                *updated_node.args,
                cst.Arg(
                    value=cst.parse_expression('"application/json"'),
                    keyword=cst.Name("content_type"),
                    equal=cst.AssignEqual(
                        whitespace_before=cst.SimpleWhitespace(""),
                        whitespace_after=cst.SimpleWhitespace(""),
                    ),
                ),
            ],
        )
