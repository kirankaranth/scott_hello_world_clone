from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from argparse import Namespace
from prophecy.test import BaseTestCase
from prophecy.test.utils import *
from job.graph.Sum_Amounts import *
import job.config.ConfigStore as ConfigStore


class Sum_AmountsTest(BaseTestCase):

    def test_unit_test_0(self):
        dfIn0 = createDfFromResourceFiles(
            self.spark,
            'test/resources/data/job/graph/Sum_Amounts/in0/schema.json',
            'test/resources/data/job/graph/Sum_Amounts/in0/data/test_unit_test_0.json',
            'in0'
        )
        dfOut = createDfFromResourceFiles(
            self.spark,
            'test/resources/data/job/graph/Sum_Amounts/out/schema.json',
            'test/resources/data/job/graph/Sum_Amounts/out/data/test_unit_test_0.json',
            'out'
        )
        dfOutComputed = Sum_Amounts(self.spark, dfIn0)
        assertDFEquals(
            dfOut.select("customer_id", "orders", "amounts", "account_length_days"),
            dfOutComputed.select("customer_id", "orders", "amounts", "account_length_days"),
            self.maxUnequalRowsToShow
        )

    def setUp(self):
        BaseTestCase.setUp(self)
        import os
        fabricName = os.environ['FABRIC_NAME']
        ConfigStore.Utils.initializeFromArgs(
            self.spark,
            Namespace(file = f"configs/resources/config/{fabricName}.json", config = None)
        )
