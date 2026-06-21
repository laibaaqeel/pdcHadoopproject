from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, avg, month, desc, round

spark = SparkSession.builder \
    .appName("ECommerceSalesAnalysis") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "file:///") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("\n" + "="*60)
print("   E-COMMERCE SALES ANALYSIS USING APACHE SPARK")
print("="*60)

df = spark.read.csv(
    "file:///workspaces/pdcHadoopproject/ecommerce_data.csv",
    header=True,
    inferSchema=True
)

print(f"\nTotal Orders Loaded: {df.count()}")

print("\n" + "-"*60)
print("ANALYSIS 1: TOP 5 BEST SELLING PRODUCTS BY REVENUE")
print("-"*60)
top_products = df.groupBy("product_name") \
    .agg(
        sum("total_amount").alias("total_revenue"),
        count("order_id").alias("total_orders")
    ) \
    .orderBy(desc("total_revenue")) \
    .limit(5)
top_products.show()

print("\n" + "-"*60)
print("ANALYSIS 2: REVENUE BY PRODUCT CATEGORY")
print("-"*60)
category_revenue = df.groupBy("category") \
    .agg(
        round(sum("total_amount"), 2).alias("total_revenue"),
        count("order_id").alias("total_orders"),
        round(avg("total_amount"), 2).alias("avg_order_value")
    ) \
    .orderBy(desc("total_revenue"))
category_revenue.show()

print("\n" + "-"*60)
print("ANALYSIS 3: SALES PERFORMANCE BY CITY")
print("-"*60)
city_revenue = df.groupBy("city", "province") \
    .agg(
        round(sum("total_amount"), 2).alias("total_revenue"),
        count("order_id").alias("total_orders")
    ) \
    .orderBy(desc("total_revenue"))
city_revenue.show()

print("\n" + "-"*60)
print("ANALYSIS 4: MONTHLY SALES TREND")
print("-"*60)
monthly_sales = df.withColumn("month", month(col("order_date"))) \
    .groupBy("month") \
    .agg(
        round(sum("total_amount"), 2).alias("monthly_revenue"),
        count("order_id").alias("total_orders")
    ) \
    .orderBy("month")
monthly_sales.show(12)

print("\n" + "-"*60)
print("ANALYSIS 5: OVERALL BUSINESS SUMMARY")
print("-"*60)
total_revenue = df.agg(round(sum("total_amount"), 2).alias("total")).collect()[0][0]
total_orders = df.count()
avg_order = df.agg(round(avg("total_amount"), 2).alias("avg")).collect()[0][0]
print(f"Total Revenue:       Rs. {total_revenue}")
print(f"Total Orders:        {total_orders}")
print(f"Average Order Value: Rs. {avg_order}")

print("\n" + "="*60)
print("   ANALYSIS COMPLETE!")
print("="*60)
spark.stop()
