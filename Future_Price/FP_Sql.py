# -*- coding: utf-8 -*- 
"""
@Time        : 2020/5/31 18:28 
@Author      : tmooming
@File        : FP_Sql.py
@Description : 实验数据入库
"""
import psycopg2
import pandas as pd
from io import StringIO



class FP_Save(object):
    def __init__(self, variable, detail):
        self.variable = variable
        self.detail = detail
        self.connection = self._connect()
        self.cur = self.connection.cursor()

    def _connect(self):
        try:
            postgres_connect = psycopg2.connect(host="127.0.0.1", port='12786', user="postgres", password="postgres",
                                                dbname="FPP")
        except:
            postgres_connect = psycopg2.connect(host="127.0.0.1", port='5432', user="postgres", password="postgres",
                                                dbname="FPP")
        return postgres_connect

    def save_data(self):
        try:
            self.cur.execute(
                "INSERT INTO public.fp_variable( futures, influence_factors, google_data_sources, time_window, f_value, time_interval) VALUES(%s,%s,%s,%s,%s,%s) returning id",
                (self.variable['futures'], self.variable['influence_factors'], self.variable['google_data_sources'],
                 self.variable['time_window'], self.variable['f_value'], self.variable['time_interval']))
            v_id = self.cur.fetchone()[0]
            print(v_id)
            output = StringIO()
            self.detail['v_id'] = [v_id] * len(self.detail)
            print(self.detail.info())

            self.detail.to_csv(output, sep='\t', index=False, header=False)
            output1 = output.getvalue()
            output1 = output1.replace('[', '{').replace(']', '}')
            self.cur.copy_from(StringIO(output1), 'public.fp_detail',
                               columns=['date', 'future', 'cfear', 'influence_factor', 'future_price', 'future_return',
                                        'v_id'])

            self.connection.commit()
            self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.connection.rollback()
            self.close()

    def close(self):
        self.cur.close()
        self.connection.close()

    # def save_detail(self, v_id):
    #     output = StringIO()
    #     self.detail['v_id'] = [v_id] * len(self.detail)
    #     print(self.detail.info())
    #
    #     self.detail.to_csv(output, sep='\t', index=False, header=False)
    #     output1 = output.getvalue()
    #     output1 = output1.replace('[', '{').replace(']', '}')
    #     self.cur.copy_from(StringIO(output1), 'public.fp_detail',
    #                        columns=['date', 'future', 'cfear', 'influence_factor', 'future_price', 'future_return',
    #                                 'v_id'])
    #
    #     self.connection.commit()
    #     self.close()


# class FP_select(object):
#     def __init__(self, sql):
#         self.sql = sql
#         self.connection = postgres_connect
#         self.cur = postgres_connect.cursor()
#
#     def get_google_trends(self):
#         df = pd.read_sql(self.sql, self.connection)  # 读取mysql中的数据
#         return df
