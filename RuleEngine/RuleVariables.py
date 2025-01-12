"""
Author: Akankshya Mohanty
Mentor & Reviewer: Rajani Vanarse
#*******************************************************************
#Copyright (C) 2023 Adino Labs
#*******************************************************************
"""
from business_rules.variables import BaseVariables, select_rule_variable


class RuleVariables(BaseVariables):
    def __init__(self, input_params):
        self.input_params = input_params

    @select_rule_variable(options=[])
    def input_params(self):
        return self.input_params
