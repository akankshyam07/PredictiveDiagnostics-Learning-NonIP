from RuleEngine.operators import StringType, NumericType, BooleanType, ListType, DictType


def get_variable_type(value):
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


def do_operator_comparison(operator_type, operator_name, comparison_value):
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
