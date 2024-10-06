"""
Rajani Vanarse
Akankshya Mohanty
"""
#*******************************************************************
#Copyright (C) 2023 Adino Labs
#*******************************************************************
from RuleConstants import RuleConstants
from operators import StringType, NumericType, BooleanType, ListType, DictType
import json


def run_all(rule_list, context):
    results = {}
    for rule in rule_list:
        result, score = run(rule, context)
        if result:
            results.update({score: rule})
    return results


def run(rule, context):
    conditions, actions = rule[RuleConstants.CONDITIONS], rule[RuleConstants.ACTIONS]
    rule_triggered, score = check_conditions_recursively(conditions, context)
    return rule_triggered, score


def check_conditions_recursively(conditions, context):
    keys = list(conditions.keys())
    if keys == [RuleConstants.AND_OPERATOR]:
        assert len(conditions[RuleConstants.AND_OPERATOR]) >= 1
        final_score = 0
        for condition in conditions[RuleConstants.AND_OPERATOR]:
            res, score = check_conditions_recursively(condition, context)
            if res:
                if score:
                    final_score += (score * condition[RuleConstants.WEIGHTAGE])
                else:
                    final_score += condition[RuleConstants.WEIGHTAGE]

        return final_score > 0, round(final_score,2)

    elif keys == [RuleConstants.OR_OPERATOR]:
        assert len(conditions[RuleConstants.OR_OPERATOR]) >= 1
        for condition in conditions[RuleConstants.OR_OPERATOR]:
            res, score = check_conditions_recursively(condition, context)
            if res:
                if score:
                    return True, round(score * condition[RuleConstants.WEIGHTAGE],2)
                else:
                    return True, condition[RuleConstants.WEIGHTAGE]
        return False, 0

    else:
        # help prevent errors - any and all can only be in the condition dict
        # if they're the only item
        assert not (RuleConstants.AND_OPERATOR in keys or RuleConstants.OR_OPERATOR in keys)
        return check_condition(conditions, context)


def check_condition(condition, defined_variables):
    """ Checks a single rule condition - the condition will be made up of
    variables, values, and the comparison operator. The defined_variables
    object must have a variable defined for any variables in this condition.
    """
    name, op, value = condition[RuleConstants.LHS_OPERAND], condition[RuleConstants.OPERATOR], condition[
        RuleConstants.RHS_OPERAND]
    operator_type = _get_variable_value(defined_variables, name)
    if not operator_type:
        return False, 0
    if isinstance(operator_type, ListType) or isinstance(operator_type, DictType):
        return _do_operator_comparison(operator_type, op, value)
    else:
        res = _do_operator_comparison(operator_type, op, value)
        if res:
            return res, 1
        else:
            return res, 0


def _get_variable_value(context, name):
    """ Call the function provided on the defined_variables object with the
    given name (raise exception if that doesn't exist) and casts it to the
    specified type.
    Returns an instance of operators.BaseType
    """

    def fallback(*args, **kwargs):
        raise AssertionError("Variable {0} is not defined in class {1}".format(
            name, context))

    value = context.get(name)
    return _get_variable_type(value)


def _get_variable_type(value):
    if type(value) == 'str':
        return StringType(value)
    elif str(value).isnumeric():
        return NumericType(value)
    elif type(value) == 'boolean':
        return BooleanType(value)
    elif isinstance(value, list) :
        return ListType(value)
    elif isinstance(value, dict):
        return DictType(value)
    else:
        return None


def _do_operator_comparison(operator_type, operator_name, comparison_value):
    """ Finds the method on the given operator_type and compares it to the
    given comparison_value.
    operator_type should be an instance of operators.BaseType
    comparison_value is whatever python type to compare to
    returns a bool
    """

    def fallback(*args, **kwargs):
        raise AssertionError("Operator {0} does not exist for type {1}".format(
            operator_name, operator_type.__class__.__name__))

    method = getattr(operator_type, operator_name, fallback)

    return method(comparison_value)


def do_actions(defined_actions):
    print(json.dumps(defined_actions))
    return defined_actions
