"""
Author: Akankshya Mohanty
Mentor & Reviewer: Rajani Vanarse
#*******************************************************************
#Copyright (C) 2023 Adino Labs
#*******************************************************************
"""
import psycopg2
import json


def open_connection():
    con = psycopg2.connect(database="postgres", user="postgres", password="password", host="127.0.0.1", port="5432")
    return con


def execute_query(query_string):
    con = open_connection()
    cur = con.cursor()
    cur.execute(query_string)
    rows = cur.fetchall()
    return rows



if __name__ == '__main__':
    query = "select disease, count(disease) from (select history_id, ph.disease from healthcare.patient_history ph " \
            "inner join healthcare.patient_symptom ps on ph.symptom_scenario_id = ps.symptom_scenario_id " \
            "inner join healthcare.labtest_result lr on ph.labtest_result_id = lr.testresult_id " \
            "where ph.patient_id = 1  and ps.symptom_ids=ARRAY[106,126,127,128,129]::bigint[] and " \
            "((lr.test_parameter_id = any(ARRAY[504,505,507]) and lr.is_abnormal = true) or " \
            "(lr.test_parameter_id = any(ARRAY[508,509]) and lr.is_abnormal = true)) " \
            "group by history_id)aggr group by aggr.disease"
    execute_query(query)
