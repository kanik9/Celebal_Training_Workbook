"""
DataFrame Related whole book.
Important Links related to DataFrames are :
pyspark.sql module : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html
    1. Topics in pyspark.sql are :
        -  'pyspark.sql.SparkSession' Main entry point for DataFrame and SQL functionality.
            Link : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.SparkSession

        -  'pyspark.sql.DataFrame' A distributed collection of data grouped into named columns.
            Link : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame

        -  'pyspark.sql.Column' A column expression in a DataFrame.
            Link : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.Column

        -  'pyspark.sql.Row' A row of data in a DataFrame.
            Link : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.Row

        -  'pyspark.sql.GroupedData' Aggregation methods, returned by DataFrame.groupBy().
            Link : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.GroupedData

        -  'pyspark.sql.DataFrameNaFunctions' Methods for handling missing data (null values).
            Link : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrameNaFunctions

        -  'pyspark.sql.DataFrameStatFunctions' Methods for statistics functionality.
            Link : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrameStatFunctions

        -  'pyspark.sql.functions' List of built-in functions available for DataFrame.
            Link : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#module-pyspark.sql.functions

        -  'pyspark.sql.types' List of data types available.
            Link : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#module-pyspark.sql.types

        -  'pyspark.sql.Window' For working with window functions.
            Link : https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.Window

"""
import math
import numpy as np

from pyspark.sql import Row
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.functions import broadcast
from pyspark.sql.types import DoubleType, IntegerType, StringType

conf = SparkConf().setMaster("local").setAppName("BigDataFirstScriptOnCovid-19")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

"""
Case.csv file contain the cases grouped by way of the infection spread. This might have helped in the rigorous tracking 
of corona cases
"""

"""Read te csv file in which the inferSchema is to get the original schema which is in data set, if you want to change 
the schema use 'Schema' instead of 'inferSchema', and the header attribute is used to use original header if its value 
is true other wise use False to not use the original header 

shape : print(cases.count(), len(cases.columns)) : (174,8)
"""
cases = spark.read.format("csv").load("../data/Case.csv",
                                      inferSchema=True,
                                      header=True,
                                      sep=","
                                      )

# To check the only top 20 rows use 'show()' method to check.
# To check specific number of lines use 'limit(n)' where n the the number of line to show.
# If the data set is too long or it contain the large number of columns then for better representation use 'toPandas()'
# print(cases.limit(10).toPandas())

# Change the column name:
"""
Step 1 is target only a single column not all.
Note : If in the large dataset the columns name contain the spaces in between them then in that case spark take little 
       bit longer time to fetch . Then the solution of this problem is that we have to change the name manually in spark
       and remove the spaces in between them to execute them fast    
"""
cases = cases.withColumnRenamed("infection_case", "infection_source")
# to change all the name of columns we have tons of methods in which one of them is :
cases = cases.toDF(*['case_id', 'province', 'city', 'group', 'infection_case', 'confirmed',
                     'latitude', 'longitude'])
# print(cases.limit(10).toPandas())

# Select Columns :
selected_cases_data = cases.select('province', 'city', 'infection_case', 'confirmed')
# print(selected_cases_data.show())

# Sort the dataSet: Note this will not update the data set
cases_sorted_in_ascending = cases.sort("confirmed")
# cases_sorted_in_ascending.show()
"""
For perform sorting in descending order we have to import a module.
from pyspark.sql import functions as F
"""
cases_sorted_in_descending = cases.sort(func.desc("confirmed"))
# cases_sorted_in_descending.show()

# Type Conversation of columns:
"""
For Performing type conversation you have to import some data types
from pyspark.sql.types import DoubleType, IntegerType, StringType
"""

cases_with_type_converted_column_confirmed = cases.withColumn("confirmed", func.col("confirmed").cast(IntegerType()))
cases_with_type_converted_column_city = cases.withColumn("city", func.col("city").cast(StringType()))

# Filter Operation :
"""
We can filter a data frame using multiple conditions using AND(&), OR(|) and NOT(~) conditions
"""

cases_filter_and_operation = cases.filter((cases.confirmed > 10) & (cases.province == "Daegu"))
# cases_filter_and_operation.show()

cases_filter_or_operation = cases.filter((cases.confirmed > 10) | (cases.province == "Daegu"))
# cases_filter_or_operation.show()

# GroupBy Operation :
# In Pyspark 'groupBy' is almost same as the pandas 'groupBy'.

cases_groupBy_operation = cases.groupBy(["province", "city"]).agg(
    func.sum("confirmed"),
    func.max("confirmed")
)
# If you want to change the column name . use alias function.
# cases.groupBy(["province","city"]).agg(
#     F.sum("confirmed").alias("TotalConfirmed"),\
#     F.max("confirmed").alias("MaxFromOneConfirmedCase")\
#     )

# cases_groupBy_operation.show()

# Joins Operations :
"""
Note : For Join operation we need two dataframes . So in this Example we use two dataframes case.csv and region.csv
Doc of Joins: 
    join(other, on=None, how=None)
    Joins with another DataFrame, using the given join expression.

        Parameters
            1. other – Right side of the join 
            2. on – a string for the join column name, a list of column names, a join expression (Column), or a list of 
                    Columns. If on is a string or a list of strings indicating the name of the join column(s), the 
                    column(s) must exist on both sides, and this performs an equi-join.
            3. how – str, default inner. Must be one of: inner, cross, outer, full, fullouter, full_outer, left, 
                     leftouter, left_outer, right, rightouter, right_outer, semi, leftsemi, left_semi, anti, leftanti 
                     and left_anti.
"""
"""
Load new data with another method. 
Data File name is Region.csv which contains region information such as elementary_school_count, elderly_population_ratio
etc.
More Details Link : https://www.kaggle.com/kimjihoo/coronavirusdataset?select=Region.csv
shape : print(regions.count(), len(regions.columns)) : (244,12)
"""

regions = spark.read.load("../data/Region.csv",
                          format="csv",
                          inferSchema=True,
                          header=True,
                          sep=","
                          )
# print(regions.limit(10).toPandas())

cases_join_operation = cases.join(regions, ["province", "city"], how="left")
# print(cases_join_operation.limit(10).toPandas())

# Broadcast/Map Slide Joins:
"""
Drawback of join : 
Note : Sometimes you might face a scenario where you need to join a very big table(~1B Rows) with a very small table
       (~100–200 rows).
Solution : Such sort of operations is aplenty in Spark where you might want to apply multiple operations to a particular
           key. But assuming that the data for each key in the Big table is large,it will involve a lot of data movement.
           And sometimes so much that the application itself breaks. A small optimization then you can do when joining 
           on such big tables(assuming the other table is small) is to broadcast the small table to each machine/node 
           when you perform a join. You can do this easily using the broadcast keyword. This has been a lifesaver many 
           times with Spark when everything else fails.
For implement Broadcast first you have to import it from pyspark.sql.functions
"""

cases_after_broadcast = cases.join(broadcast(regions), ["province", "city"], how="left")
# print(cases_after_broadcast.limit(10).toPandas())

# Use SQL Queries with DataFrames
cases.registerTempTable("cases_table")
newDf = spark.sql("""
                       select * 
                       from cases_table
                       where confirmed > 100
                       """)
# print("DataFrame Execute by SQL Query : \n")
# newDf.show()

# Create New Columns

"""
There are many ways that you can use to create a column in a PySpark Dataframe.
    1. Using Spark Native Functions {withColumn}
    2. Using Spark UDFs 
    3. Using RDDs
    4. Using Pandas UDF
"""

"""
1. Using Spark Native Functions {withColumn} : 
"""

casesWithNewConfirmed = cases.withColumn("NewConfirmed", 100 + func.col("confirmed"))
# casesWithNewConfirmed.show()

casesWithExpConfirmed = cases.withColumn("ExpConfirmed", func.exp("confirmed"))
# casesWithExpConfirmed.show()

"""
2. Using Spark UDFs : 
        Sometimes we want to do complicated things to a column or multiple columns.This could be thought of as a map 
        operation on a PySpark Dataframe to a single column or multiple columns. While Spark SQL functions do solve many
        use cases when it comes to column creation, I use Spark UDF whenever I need more matured Python functionality.
"""


def casesHighLow(confirmed):
    if confirmed < 50:
        return "Low"
    else:
        return "High"


# Convert to a UDF Function by passing in the function and return type of function
casesHighLowUDF = func.udf(casesHighLow, StringType())
casesWithHighLow = cases.withColumn("HighLow", casesHighLowUDF("confirmed"))
# casesWithHighLow.show()

"""
3. Using RDDs : 
    1. This might seem a little odd, but sometimes both the spark UDFs and SQL functions are not enough for a particular
       use-case. I have observed the RDDs being much more performant in some use-cases in real life.
"""


def rowwise_function(row):
    row_dict = row.asDict()
    row_dict["expConfirmed"] = float(np.exp(row_dict["confirmed"]))
    newrow = Row(**row_dict)
    return newrow


# convert cases dataframe to RDD
cases_rdd = cases.rdd

cases_rdd_new = cases_rdd.map(lambda row: rowwise_function(row))
# convert RDD back to DataFrame
casesNewDf = spark.createDataFrame(cases_rdd_new)
# casesNewDf.show()


"""
Load one more data for explaining the spark window function.
Data File name is TimeProvince.csv which contains Time series data of COVID-19 status in terms of the Province


"""

time_province = spark.read.load("../data/TimeProvince.csv",
                          format="csv",
                          inferSchema=True,
                          header=True,
                          sep=","
                          )
print(time_province.limit(10).toPandas())
