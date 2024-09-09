import os
import re
import pandas as pd
import pdfplumber as pb
import time
#####  Self - Design Class and Functions #####
from Extractor import Extractor
from InvoiceDetector import InvoiceDetector
from DataCleaner import DataCleaner
#############################################

def main():
    start_time = time.time()
    path = 'invoice_2'
    detector = InvoiceDetector(path)
    detector.Detect()
    detector.Clean()
    detector.Check_Error_List()
    end_time = time.time()
    print('\n =============================\n')
    execution_time = end_time - start_time
    print("All Done!")
    detector.Save('InvoiceList.xlsx')
    print(f"发票检测程序运行时间: {execution_time} 秒")
    print("The undetected files are :")
    detector.Check_Error_List()
    detector.Showinfo()
    
if __name__ == '__main__':
    main()