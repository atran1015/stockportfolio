from cmath import exp
import unittest
#from unittest.mock import patch
import yfinance as yf
from stockinfo import *
import json
import pandas as pd
import numpy as np
import pandas.testing as pd_testing

with open("stockinfomock.json") as fh:
            stock = json.load(fh)

class MockStock():
    def __init__(self):
        self.recommendations = pd.read_csv("recommendations.csv", index_col=[0])
    def history(self, **args):
        df = pd.read_csv("history.csv", index_col=[0])
        return df

class TestSelectStock(unittest.TestCase):
    
    def testPrintHistoricalAndRec(self):
        stock = MockStock()
        val = PrintHistoricalAndRec(stock)
        expected = pd.read_csv("concat_data.csv", index_col=[0])
        pd_testing.assert_frame_equal(val, expected)
        print("Passed")
    

    def testPrintPERatios(self):
        a, b = PrintPERatios(stock)
        expected_a = 5.503817
        expected_b = 6.838753
        self.assertEqual(a, expected_a)
        self.assertEqual(b, expected_b)
        print("Passed")
    
    
    def testPrintAsk(self):
        val = PrintAsk(stock)
        expected = 0
        self.assertEqual(val , expected)
        print("Passed")

    
    def testPrintBid(self):
        val = PrintBid(stock)
        expected = 0
        self.assertEqual(val , expected)
        print("Passed")

    def testPrintEPS(self):
        val = PrintEPS(stock)
        expected = 78.74
        self.assertEqual(val, expected)
        print("Passed")
        
 
if __name__ == '__main__':
    unittest.main()