from DataCleaner import DataCleaner
import os
import re
import pandas as pd
import pdfplumber as pb
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

    def Add(self,invoice):
        print("Adding Invoice...")
        ## DB Operation
            #需要齐硕哥哥
        ###

    def Save(self,dest):
        self.InvoiceList.to_excel(dest)
        print("Data Saved! -- path: " + str(dest))

    def Showinfo(self):
        print("Welcome to use InvoiceDetector(Version 1.0)")
        print(f"Valid Invoice Count: {self.valid_count-1}")
        print(f"Error Invoice Count: {len(self.ErrorList)}, Please check them manually")
        return self.valid_count-1, len(self.ErrorList), self.ErrorList
