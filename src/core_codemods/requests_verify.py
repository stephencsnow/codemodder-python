from codemodder.codemods.libcst_transformer import NewArg
from core_codemods.api import (
    Metadata,
    Reference,
    ReviewGuidance,
    SimpleCodemod,
)


class RequestsVerify(SimpleCodemod):
    metadata = Metadata(
        name="requests-verify",
        summary="Verify SSL Certificates for Requests.",
        review_guidance=ReviewGuidance.MERGE_AFTER_CURSORY_REVIEW,
        references=[
            Reference(url="https://requests.readthedocs.io/en/latest/api/"),
            Reference(
                url="https://owasp.org/www-community/attacks/Manipulator-in-the-middle_attack"
            ),
        ],
    )
    change_description = (
        "Makes any calls to requests.{func} with `verify=False` to `verify=True`."
    )
    detector_pattern = """
        rules:
          - patterns:
            - pattern: requests.$F(..., verify=False, ...)
            - pattern-inside: |
                import requests
                ...
        """

    def on_result_found(self, original_node, updated_node):
        new_args = self.replace_args(
            original_node, [NewArg(name="verify", value="True", add_if_missing=False)]
        )
        return self.update_arg_target(updated_node, new_args)
