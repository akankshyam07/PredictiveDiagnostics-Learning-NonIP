import json

class Rule_Builder:

    def __init__(self):
        pass

    def create_rules(self, rule_json_file):
        if not rule_json_file:
            with open(rule_json_file) as json_file:
                rule_list = json.load(json_file)