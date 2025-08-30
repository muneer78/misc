# Databricks notebook source
from pyspark.sql.types import StructType

# get field name from schema (recursive for getting nested values)
def get_schema_field_name(field, parent=None):
  if type(field.dataType) == StructType:
    if parent == None:
      prt = field.name
    else:
      prt = parent+"."+field.name # using dot notation
    res = []
    for i in field.dataType.fields:
      res.append(get_schema_field_name(i, prt))
    return res
  else:
    if parent==None:
      res = field.name
    else:
      res = parent+"."+field.name
    return res
  
# flatten list, from https://stackoverflow.com/a/12472564/4920394
def flatten(S):
  if S == []:
    return S
  if isinstance(S[0], list):
    return flatten(S[0]) + flatten(S[1:])
  return S[:1] + flatten(S[1:])

# list of databases
db_list = [x[0] for x in spark.sql("SHOW DATABASES").rdd.collect()]

for i in db_list:
  spark.sql("SHOW TABLES IN {}".format(i)).createOrReplaceTempView(str(i)+"TablesList")

# create a query for fetching all tables from all databases
union_string = "SELECT database, tableName FROM "
for idx, item in enumerate(db_list):
  if idx == 0:
    union_string += str(item)+"TablesList WHERE isTemporary = 'false'"
  else:
    union_string += " UNION ALL SELECT database, tableName FROM {}".format(str(item)+"TablesList WHERE isTemporary = 'false'")
spark.sql(union_string).createOrReplaceTempView("allTables")

# full list = schema, table, column
full_list = []
for i in spark.sql("SELECT * FROM allTables").collect():
  table_name = i[0]+"."+i[1]
  table_schema = spark.sql("SELECT * FROM {}".format(table_name))
  column_list = []
  for j in table_schema.schema:
    column_list.append(get_schema_field_name(j))
  column_list = flatten(column_list)
  for k in column_list:
    full_list.append([i[0],i[1],k])
spark.createDataFrame(full_list, schema = ['database', 'tableName', 'columnName']).createOrReplaceTempView("allColumns")```