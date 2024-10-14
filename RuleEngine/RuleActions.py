"""
Author: Akankshya Mohanty
Mentor & Reviewer: Rajani Vanarse
#*******************************************************************
#Copyright (C) 2023 Adino Labs
#*******************************************************************
"""
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT


class RuleActions(BaseActions):
    def __init__(self, params):
        self.params = params

    @rule_action(params={"params": FIELD_TEXT})
    def execute_rule(self, params):
        print(params)