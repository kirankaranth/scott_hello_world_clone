from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from job.config.ConfigStore import *
from job.udfs.UDFs import *
from prophecy.utils import *
from job.graph import *

def pipeline(spark: SparkSession) -> None:
    df_Orders = Orders(spark)
    df_Orders = collectMetrics(spark, df_Orders, "graph", "Source_28006", "65082")
    df_Customers = Customers(spark)
    df_Customers = collectMetrics(spark, df_Customers, "graph", "Source_51275", "83296")
    df_By_CustomerId = By_CustomerId(spark, df_Orders, df_Customers)
    df_By_CustomerId = collectMetrics(spark, df_By_CustomerId, "graph", "Join_98619", "31576")
    df_Cleanup = Cleanup(spark, df_By_CustomerId)
    df_Cleanup = collectMetrics(spark, df_Cleanup, "graph", "Reformat_5054", "16363")
    df_Sum_Amounts = Sum_Amounts(spark, df_Cleanup)
    df_Sum_Amounts = collectMetrics(spark, df_Sum_Amounts, "graph", "Aggregate_74495", "96556")
    Customer_Orders(spark, df_Sum_Amounts)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    MetricsCollector.initializeMetrics(spark)
    spark.conf.set("prophecy.collect.basic.stats", "true")
    spark.conf.set("spark.sql.legacy.allowUntypedScalaUDF", "true")
    spark.conf.set("spark.sql.optimizer.excludedRules", "org.apache.spark.sql.catalyst.optimizer.ColumnPruning")
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/customers_orders")
    
    MetricsCollector.start(
        spark = spark,
        pipelineId = spark.conf.get("prophecy.project.id") + "/" + "pipelines/customers_orders"
    )
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
