from apriori_starter import go
import pytest
from unittest import TestCase

class AprioriTest(TestCase):
    def test_apriori_min_sup_5_percent(self):
        go('code/BMS1_spmf.txt',0.05)

    def test_apriori_min_sup_1_percent(self):
        go('code/BMS1_spmf.txt',0.01)

    def test_apriori_min_sup_3_percent(self):
        go('code/BMS1_spmf.txt',0.03)
