from pymadlib.pymadlib import *
from pymadlib import example
from pymadlib.example import *

conn_str = '''host='{hostname}' port ='{port}' dbname='{database}' user='{username}' password='{password}' '''
#conn_str = conn_str.format(hostname='localhost',database='pivotal_test',port='5433',username='gpadmin',password='gpadmin')
conn_str = conn_str.format(hostname='localhost',database='madlib_test',port='5432',username='postgres',password='antarone')

#PyMADlib is compatible with only MADlib v0.5, so we need to explicitly specify the MADlib schema.
#We have installed both MADlib 1.3 and MADlib 0.5 in this VM.
conn = DBConnect(conn_str=conn_str,madlib_schema='madlib_v05')

