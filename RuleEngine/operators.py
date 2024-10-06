"""
Rajani Vanarse
Akankshya Mohanty
"""
#*******************************************************************
#Copyright (C) 2023 Adino Labs
#*******************************************************************
import inspect
import re
from decimal import Decimal


class BaseType(object):
    def __init__(self, value):
        self.value = self._assert_valid_value_and_cast(value)

    def _assert_valid_value_and_cast(self, value):
        raise NotImplemented()

    @classmethod
    def get_all_operators(cls):
        methods = inspect.getmembers(cls)
        return [{'name': m[0],
                 'label': m[1].label,
                 'input_type': m[1].input_type}
                for m in methods if getattr(m[1], 'is_operator', False)]


class StringType(BaseType):

    name = "string"

    def _assert_valid_value_and_cast(self, value):
        value = value or ""
        if not type(value) == 'str':
            raise AssertionError("{0} is not a valid string type.".
                                 format(value))
        return value

    def equals(self, other_string):
        return self.value == other_string

    def equals_ignorecase(self, other_string):
        return self.value.lower() == other_string.lower()

    def startswith(self, other_string):
        return self.value.startswith(other_string)

    def endswith(self, other_string):
        return self.value.endswith(other_string)

    def contains(self, other_string):
        return other_string in self.value

    def matches_regex(self, regex):
        return re.search(regex, self.value)

    def non_empty(self):
        return bool(self.value)

    def IN(self, other_obj):
        return self.value in other_obj


class NumericType(BaseType):
    EPSILON = Decimal('0.000001')

    name = "numeric"

    def _assert_valid_value_and_cast(self, value):
        if not str(value).isnumeric():
            raise AssertionError("{0} is not a valid numeric type.".
                                 format(value))
        return value

    def equals(self, other_numeric):
        return abs(self.value - other_numeric) <= self.EPSILON

    def gt(self, other_numeric):
        return (self.value - other_numeric) > self.EPSILON

    def gte(self, other_numeric):
        return self.gt(other_numeric) or self.equals(other_numeric)

    def lt(self, other_numeric):
        return (other_numeric - self.value) > self.EPSILON

    def lte(self, other_numeric):
        return self.lt(other_numeric) or self.equals(other_numeric)

    def IN(self, other_obj):
        return self.value in other_obj


class BooleanType(BaseType):

    name = "boolean"

    def _assert_valid_value_and_cast(self, value):
        if type(value) != bool:
            raise AssertionError("{0} is not a valid boolean type".
                                 format(value))
        return value

    def is_true(self):
        return self.value

    def is_false(self):
        return not self.value


class ListType(BaseType):
    name = "list"

    def _assert_valid_value_and_cast(self, value):
        if not isinstance(value, list):
            raise AssertionError("{0} is not a valid list type".
                                 format(value))
        return value

    def IN(self, other_obj):
        if isinstance(self.value, list):
            count = 0
            for item in self.value:
                if item in other_obj:
                    count += 1
            return (count > 0), count/len(other_obj)
        else:
            return self.value in other_obj

    def equals(self, other_obj):
        for item in self.value:
            if type(item) == type(other_obj):
                operator_type = get_variable_type(other_obj)
                if operator_type:
                    if isinstance(operator_type, ListType) or isinstance(operator_type, DictType):
                        res, score = do_operator_comparison(operator_type, 'equals', item)
                        if res:
                            return res, score
                else:
                    res = do_operator_comparison(operator_type, 'equals', item)
                    if res:
                        return res, 1

        return False, 0


class DictType(BaseType):
    name = "dict"

    def _assert_valid_value_and_cast(self, value):
        if not isinstance(value, dict):
            raise AssertionError("{0} is not a valid list type".
                                 format(value))
        return value

    def equals(self, other_obj):
        if isinstance(self.value, dict):
            count = 0
            for key, value in self.value.items():
                if isinstance(other_obj, dict):
                    if key == 'name' and value != other_obj[key]:
                        break
                    if key in other_obj.keys():
                        if isinstance(value, list) and other_obj[key] in value:
                            count += 1
                        elif value == other_obj[key]:
                            count += 1
                elif isinstance(other_obj, list):
                    res, percent = False, 0
                    for other_item in other_obj:
                        res, percent = self.equals(other_item)
                        if res:
                            break
                    return res, percent
            return (count > 0), count/len(set(self.value).intersection(set(other_obj)))
        else:
            return False, 0


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