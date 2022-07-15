import unittest
import yfinance as yf
 
class SelectStock(unittest.TestCase):
 
    def testDownload(self):
        self.assertNotEqual(yf,'None')
 
if __name__ == '__main__':
    unittest.main()