from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from argparse import Namespace
from prophecy.test import BaseTestCase
from prophecy.test.utils import *
from job.graph.Cleanup import *
import job.config.ConfigStore as ConfigStore


class CleanupTest(BaseTestCase):

    def test_unit_test_0(self):
        dfIn0 = createDfFromResourceFiles(
            self.spark,
            'test/resources/data/job/graph/Cleanup/in0/schema.json',
            'test/resources/data/job/graph/Cleanup/in0/data/test_unit_test_0.json',
            'in0'
        )
        dfOut = createDfFromResourceFiles(
            self.spark,
            'test/resources/data/job/graph/Cleanup/out/schema.json',
            'test/resources/data/job/graph/Cleanup/out/data/test_unit_test_0.json',
            'out'
        )
        dfOutComputed = Cleanup(self.spark, dfIn0)
        assertDFEquals(
            dfOut.select("account_length_days", "order_id", "customer_id", "amount"),
            dfOutComputed.select("account_length_days", "order_id", "customer_id", "amount"),
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
