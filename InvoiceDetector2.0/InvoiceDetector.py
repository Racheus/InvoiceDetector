from DataCleaner import DataCleaner
import os
import re
import pandas as pd
import numpy as np
import pdfplumber as pb
import pymysql
from sqlalchemy import create_engine
class InvoiceDetector(object):
    def __init__(self, path):
        self.folder_path = path
        self.InvoiceList = pd.DataFrame()
        self.ErrorList = []
        self.valid_count = 1

    def Clean(self):
        self.InvoiceList = self.InvoiceList.T
        for item in self.InvoiceList['购买方名称']:
            if str(item).find('名称：') != -1:
                replace = item.split('名称：')[1]
                self.InvoiceList['购买方名称'] = self.InvoiceList['购买方名称'].replace(item, replace)

        for item in self.InvoiceList['购买方纳税人识别号']:
            if str(item).find('纳税人识别号：') != -1:
                replace = item.split('纳税人识别号：')[1]
                self.InvoiceList['购买方纳税人识别号'] = self.InvoiceList['购买方纳税人识别号'].replace(item, replace)

        for item in self.InvoiceList['销售方名称']:
            if str(item).find('名称：') != -1:
                replace = item.split('名称：')[1]
                self.InvoiceList['销售方名称'] = self.InvoiceList['销售方名称'].replace(item, replace)

        for item in self.InvoiceList['销售方纳税人识别号']:
            if str(item).find('纳税人识别号：') != -1:
                replace = item.split('纳税人识别号：')[1]
                self.InvoiceList['销售方纳税人识别号'] = self.InvoiceList['销售方纳税人识别号'].replace(item, replace)
                
    def check_PDF_num(self):
        pdf_num = 0
        for file in os.listdir(self.folder_path):
            if file.endswith('.pdf'):
                pdf_num += 1
        return pdf_num
    
    def Detect(self):
        for file in os.listdir(self.folder_path):
            if file.endswith('.pdf'):
                path = os.path.join(self.folder_path, file)
                try:
                    cleaner = DataCleaner(path)
                    cleaned_data = cleaner.Clean_Single_invoice()
                    cleaned_data.columns = ['Invoice'+str(self.valid_count)]
                    self.valid_count += 1
                    self.InvoiceList = pd.concat([self.InvoiceList, cleaned_data], axis=1)
                    print(f"=={file}== have been loaded")
                except Exception as e:
                    print(f"Error processing file {file}: {e},NEED MANUAL CHECK")
                    self.ErrorList.append(file)
    def Check_Error_List(self):
        print(f"Error List: {self.ErrorList}")


    def Save(self,dest):
        self.InvoiceList.to_excel(dest)
        print("Data Saved! -- path: " + str(dest))

    def Showinfo(self,user_name,user_password):
        print("Welcome to use InvoiceDetector(Version 1.0)")
        print(f"Valid Invoice Count: {self.valid_count-1}")
        print(f"Error Invoice Count: {len(self.ErrorList)}, Please check them manually")
        self.InvoiceList = self.InvoiceList.replace(np.nan, 'empty')
        db = pymysql.connect(
            host="localhost",
            user=user_name,
            password=user_password,
            database="db_Invoice")
        cursor = db.cursor()
        for row in self.InvoiceList.iterrows():
            cursor.execute("INSERT INTO tb_invoice(invoice_code, date, buyer_code, buyer_name, seller_code, seller_name, invoice_amount_SMALL, note) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (row[1]['发票号码'], row[1]['开票日期'], row[1]['购买方纳税人识别号'], row[1]['购买方名称'], row[1]['销售方纳税人识别号'], row[1]['销售方名称'], row[1]['价税合计(小写)'], row[1]['备注']))
        db.commit()
        db.close()

        return self.valid_count-1, len(self.ErrorList), self.ErrorList
