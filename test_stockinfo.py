import unittest
#from unittest.mock import patch
import io
import sys
import yfinance as yf
from stockinfo import *

# test function only, check to see if it returns accurate results or not 

class SelectStock(unittest.TestCase):

    @staticmethod
    def testPrintHistoricalAndRec():
        capturedOutput = io.StringIO()                  # Create StringIO object
        sys.stdout = capturedOutput                     #  and redirect stdout.
        stock = yf.Ticker("DOW")
        PrintHistoricalAndRec(stock)
        sys.stdout = sys.__stdout__                     # Reset redirect.
        print ('Captured', capturedOutput.getvalue())   # Now works as before.

    @staticmethod
    def testPrintPERatios():
        capturedOutput = io.StringIO()                  # Create StringIO object
        sys.stdout = capturedOutput                     #  and redirect stdout.
        stock = yf.Ticker("DOW")
        PrintPERatios(stock)
        sys.stdout = sys.__stdout__                     # Reset redirect.
        print ('Captured', capturedOutput.getvalue())   # Now works as before.
    
    @staticmethod
    def testPrintAsk():
        capturedOutput = io.StringIO()                  # Create StringIO object
        sys.stdout = capturedOutput                     #  and redirect stdout.
        stock = yf.Ticker("DOW")
        PrintAsk(stock)
        sys.stdout = sys.__stdout__                     # Reset redirect.
        print ('Captured', capturedOutput.getvalue())   # Now works as before.

    @staticmethod
    def testPrintBid():
        capturedOutput = io.StringIO()                  # Create StringIO object
        sys.stdout = capturedOutput                     #  and redirect stdout.
        stock = yf.Ticker("DOW")
        PrintBid(stock)
        sys.stdout = sys.__stdout__                     # Reset redirect.
        print ('Captured', capturedOutput.getvalue())   # Now works as before.

    @staticmethod
    def testPrintEPS():
        capturedOutput = io.StringIO()                  # Create StringIO object
        sys.stdout = capturedOutput                     #  and redirect stdout.
        stock = yf.Ticker("DOW")
        PrintEPS(stock)
        sys.stdout = sys.__stdout__                     # Reset redirect.
        print ('Captured', capturedOutput.getvalue())   # Now works as before.
 
if __name__ == '__main__':
    unittest.main()