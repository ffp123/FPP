'''
该模块为整个程序的输入模块，输入起始日期，输入结束日期，输入期货品种

'''
import sys

sys.path.append("..")
from dateutil.parser import parse
from FutureDatebase import dateBase
import pandas as pd
#期货品种
futureDatabase = ['AL','CU','RU','A','WT','M','WS','CF','FU','C',
                                 'B','SR','Y','TA','ZN','RO','L','P','AU','RB','WR','ER','V','IF','PB','J','ME','PM','AG','OI',
                                 'RI','WH','FG','RM','RS','JM','TF','TC','BU','I','JD','JR','BB','FB','PP','HC','MA','LR','SF',
                                 'SM','CS','T','NI','SN','IC','IH','ZC','CY','AP','SC','TS','SP','EG','CJ','UR','NR','RR',
                                 'SS','EB','SA','PG']
def get_date():
	input_date_str = input('input the begin date from [ 2010-01-11: 2020-05-08]: ')
	input_date = parse(input_date_str)
	date0 = input_date.strftime('%Y-%m-%d')
	while (date0 not in dateBase):
		input_date_str = input('the date is not weekday, please input other: ')
		input_date = parse(input_date_str)


	end_date_str = input('input the end date from [ 2010-01-11: 2020-05-08]: ')
	end_date = parse(end_date_str)
	date1 = end_date.strftime('%Y-%m-%d')
	# sprint(date)
	# weekday = input_date.weekday()
	while (date1 not in dateBase):
		end_date_str = input('the date is not weekday, please input other: ')
		end_date = parse(end_date_str)
		weekday = input_date.weekday()

	return input_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def get_future():
	print('Futures: AL,CU,RU,A,WT,M,WS,CF,FU,C,B,SR,Y,TA,ZN,RO,L,P,AU,RB,WR,ER,V,IF,PB,J,ME,PM,AG,OI,RI,WH,FG,RM,RS,JM,TF,TC,BU,I,JD,JR,BB,FB,PP,HC,MA,LR,SF,SM,CS,T,NI,SN,IC,IH,ZC,CY,AP,SC,TS,SP,EG,CJ,UR,NR,RR,SS,EB,SA,PG')
	future = input('input the future[Capital letters]: ')
	while (future not in futureDatabase):
		future = input('please re-input existing future[Capital letters]: ')
	return future

startTime, endTime = get_date()
future = get_future()
# print(startTime)
# print(endTime)
#print(future)