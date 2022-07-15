import unittest
import yfinance as yf
import stockinfo
 
class SelectStock(unittest.TestCase):
 
    def testDownload(self):
        self.assertNotEqual(yf,'None')
    # test function only, check to see if it returns accurate results or not
 
if __name__ == '__main__':
    unittest.main()