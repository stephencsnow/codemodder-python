from core_codemods.api import (
    Metadata,
    ReviewGuidance,
    SimpleCodemod,
)


class MoveEnum(SimpleCodemod):
    metadata = Metadata(
        name="move-enum",
        review_guidance=ReviewGuidance.MERGE_WITHOUT_REVIEW,
        summary="Move enum members",
        references=[],
    )

    _old_enum = "LaunchDarklyFlagType"
    _new_enum = "BusinessSetting"
    _new_enum_module = "suma.apps.feature_flags.enums"

    detector_pattern = f"""
        rules:
          - patterns:
            - pattern: {_old_enum}.$MEMBER
            - metavariable-pattern:
                metavariable: $MEMBER
                patterns:
                - pattern-either:
                  - pattern: FRAUD_MOBILE_ALERTS_ENABLED
                  - pattern: REQUEST_MANUAL_BANK_STATEMENTS

    """

    change_description = "Move {member} from old enum to new enum"

    def on_result_found(self, original_node, updated_node):
        self.remove_unused_import(original_node)
        self.add_needed_import(module=self._new_enum_module, obj=self._new_enum)
        return self.update_attribute_value(updated_node, self._new_enum)
