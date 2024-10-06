from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT


class RuleActions(BaseActions):
    def __init__(self, params):
        self.params = params

    @rule_action(params={"params": FIELD_TEXT})
    def execute_rule(self, params):
        print(params)