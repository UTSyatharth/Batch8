from pyspark.sql import SparkSession
from pyspark.sql.functions import col, collect_list, concat_ws

spark = SparkSession.builder \
    .appName("Spark Assignment") \
    .getOrCreate()


file_path = "/Users/shrutisharma/PycharmProjects/Batch8/mypandasmodule/Input_data.csv"

# 1) Read the Input_data CSV file into pyspark dataframe using.
df = spark.read.csv(file_path, header=True, inferSchema=True)

df.show()





# 2) Create a new dataframe "df_out" by adding new column "Web_TREE" as shown in the output_data sheet.

from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("Web_TREE").getOrCreate()

df = spark.read.option("header",True).csv(file_path)

# Defining  window function
window_1 = Window.partitionBy("DVISION_ID", "CLASS_ID", "BRAND_ID").orderBy("PARENT_CATEGORY_ID")

# Creating "Web_TREE" column
df_out = df.withColumn("Web_TREE", F.concat_ws("_", F.collect_list("PARENT_CATEGORY_ID").over(window_1)))

df_out.show(truncate=False)

# Saving output to CSV
output1_file = "/Users/shrutisharma/PycharmProjects/Batch8/mypandasmodule/Output1_data.csv"  # Update with actual path
df_out.write.csv(output1_file, header=True, mode="overwrite")



# 3) Write the "df_out" dataframe as JSON file in "./out/json" directory.

df_out.coalesce(1).write.mode("overwrite").json("/Users/shrutisharma/PycharmProjects/Batch8/mypandasmodule/out/json")




# 4)Write the "df_out" dataframe as Parquet file in "./out/json" directory.

df_out.coalesce(1).write.mode("overwrite").parquet("./out/json/parquet")












