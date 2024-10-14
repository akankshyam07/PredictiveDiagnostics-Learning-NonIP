"""
Author: Akankshya Mohanty
Mentor & Reviewer: Rajani Vanarse
#*******************************************************************
#Copyright (C) 2023 Adino Labs
#*******************************************************************
"""
import RuleExecutor, Mongo_config
from Recommendation import Recommendation
from RuleConstants import RuleConstants
import json
import glob

def get_correlated_param_evaluation(merged_report_parameters, lab_test_rules):
    result = RuleExecutor.run_all(lab_test_rules, merged_report_parameters)
    sorted_res = sorted(result, reverse=True)
    return result[sorted_res[0]], sorted_res[0]


def get_historical_prediction(is_self):
    if is_self:
        query = self_history_query
    else:
        query = others_history_query
    rows = Postgres_connections.execute_query(query)
    total = 0
    disease_dict = {}
    for row in rows:
        total += row[1]
        disease_dict[row[0][0]] = row[1]
    new_dict = {}
    for key, value in disease_dict.items():
        val = round(value / total, 2)
        new_dict[val] = key
    sorted_dict = sorted(new_dict, reverse=True)
    return new_dict[sorted_dict[0]], sorted_dict[0]


def test_rule_executor():
    data = {
        "symptom": [
            {
                "name": "fever",
                "severity": "medium",
                "duration": "3-5 days"
            },
            {
                "name": "cough"
            },
            {
                "name": "headache"
            }
        ]
    }

    with open("./test_rules/Diagnosis_rules.json") as f:
        all_rules = json.load(f)
        rules = []
        for rule in all_rules:
            if rule[RuleConstants.RULE_TYPE] == RuleConstants.SYMPTOM_RULE:
                rules.append(rule)
    # rules = read(Mongo_config.DB, Mongo_config.COLLECTION, {'type': 'SYMPTOM'})
    result = RuleExecutor.run_all(rules, data)
    sorted_result = sorted(result, reverse=True)
    print("############## Top 2 matching rules: ####################")
    for key in sorted_result[:2]:
        print("\nPredictions: {}. Score : {}".format(result[key][RuleConstants.ACTIONS], key))

    rule = result[sorted_result[0]]
    if Recommendation.TESTS.name in rule[RuleConstants.ACTIONS]:
        action = input("\nDo you want to book/recommend test?Y/N: ")
        if action.lower().startswith("y"):
            print("\n####### Test/s booked.: {}".format(rule[RuleConstants.ACTIONS][Recommendation.TESTS.name]))
            test_report_path = input("\nPlease provide the path for test report file: ")
            test_reports = []
            for file in glob.glob(test_report_path + "**/*.json"):
                with open(file) as json_file:
                    test_reports.append(json.load(json_file))
            print("\nFound {} test reports".format(len(test_reports)))
            print("\n############### Executing Rules against test reports ##########################")
            with open("./test_rules/Diagnosis_rules_test_report.json") as f1:
                    lab_test_rules = json.load(f1)

            merged_report_parameters = {}
            final_predictions = {}
            for report in test_reports:
                merged_report_parameters.update(report)
                result = RuleExecutor.run_all(lab_test_rules, report)
                sorted_result = sorted(result, reverse=True)
                print("\n######################## Top 2 predictions from Test report : {}".format(report["test_name"]))
                for key in sorted_result[:2]:
                    probable_disease = result[key][RuleConstants.ACTIONS][Recommendation.PROBABLE_DISEASE.name][0]
                    print("Predictions: {}. Score : {}".format(probable_disease, key))
                    if probable_disease in final_predictions:
                        if final_predictions[probable_disease] < key:
                            final_predictions[probable_disease] = round(key, 2)
                    else:
                        final_predictions[probable_disease] = round(key, 2)

            # Correlated parameter evaluation
            correlated_prediction, correlation_score = get_correlated_param_evaluation(merged_report_parameters,
                                                                                       lab_test_rules)
            correlated_prediction_disease = \
                correlated_prediction[RuleConstants.ACTIONS][Recommendation.PROBABLE_DISEASE.name][0]
            print("\n############# Correlated parameter evaluation result. ################")
            print("Predictions: {}. Score : {}".format(correlated_prediction_disease, correlation_score))
            print("Increasing score of {}".format(correlated_prediction_disease))
            if correlated_prediction_disease in final_predictions:
                final_predictions[correlated_prediction_disease] = round(
                    final_predictions[correlated_prediction_disease] + 0.1, 2)

            print("\n############ Final recommendations: ")
            for key, value in final_predictions.items():
                print("Probabale Disease: {}, Score : {}".format(key, value))
        elif action.lower().startswith("n"):
            print("No further action taken.")
    else:
        pass


if __name__ == '__main__':
    test_rule_executor()
