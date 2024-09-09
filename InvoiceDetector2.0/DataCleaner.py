from Extractor import Extractor
import os
import re
import pandas as pd
import pdfplumber as pb
class DataCleaner(object):
    def __init__(self, path):
        self.path = path
        self.file = path if os.path.isfile else None
        self.data = Extractor(path).extract().T
        self.Invoicedata = pd.DataFrame()
        self.ErrorList = []

       
    def _check_type(self):
        with pb.open(self.path) as pdf:
            p0 = pdf.pages[0]
            text = p0.extract_text()
            lines = text.splitlines()
            type_of_invoice = lines[0]

            if type_of_invoice.find('电子发票（普通发票）') != -1:
                return 1;
            elif type_of_invoice.find('电⼦发票（增值税专用发票）') != -1:
                return 2;
            elif type_of_invoice.find('增值税电子普通发票') != -1:
                return 3;
            else:
                return 4; #other types,可能需要人工处理

    def data_clean_normal(self):
         # i. 无效ASCII·字符清除
        self.data.columns = ['Details']
        self.data['Details'] =  self.data['Details'].str.replace('\n', '')
        #ii.重复定位数据清除
        for item in  self.data['Details']:
            #这里非常变态，可能是中文的冒号或者英文
            if '：' in item:
                index = item.index('：')
                cleaned = item[index+1:]
                self.data['Details'] =  self.data['Details'].replace(item, cleaned)
                print("Repeated opeartor cleaned once.")
        #iii. 重新整理备注信息，因为在电子发票中，备注信息可能含有银行、银行账号等关键信息
        for item in self.data['Details']:
            if re.search(r'销方开户银行', item):
                #这里是有可能是中文冒号！
                if '：' in item.split(';')[0]:
                    self.data.loc['销售方开户行及账号'] = item.split(';')[0].split('：')[1];
                else:
                    self.data.loc['销售方开户行及账号'] = item.split(';')[0].split(':')[1];
            if re.search(r'银行账号', item):
                if '：' in item.split(';')[0]:
                    self.data.loc['销售方开户行及账号'] += item.split(';')[1].split('：')[1];
                else:
                    self.data.loc['销售方开户行及账号'] += item.split(';')[1].split(':')[1];
        self.data.loc['备注']=''
    
    def data_clean_zzs_normal(self):
        # i. 无效ASCII·字符清除
        self.data.columns = ['Details']
        self.data['Details'] = self.data['Details'].str.replace('\n', '')
        #ii.重复定位数据清除
        for item in self.data['Details']:
            #这里非常变态，可能是中文的冒号或者英文
            if '：' in item:
                index = item.index('：')
                cleaned = item[index+1:]
                self.data['Details'] = self.data['Details'].replace(item, cleaned)
                print("Repeated opeartor cleaned once.")
        #iii. 重新整理备注信息，因为在电子发票中，备注信息可能含有银行、银行账号等关键信息
        for item in self.data['Details']:
            if item.find('销方开户银行') != -1:
                #这里是有可能是中文冒号！
                if '：' in item.split('销方开户银行')[1]:
                    self.data.loc['销售方开户行及账号'] = item.split('销方开户银行：')[1].split(';')[0] + item.split('银行账号：')[1].split(';')[0]
                else:
                    self.data.loc['销售方开户行及账号'] = item.split('销方开户银行:')[1].split(';')[0] + item.split('银行账号:')[1].split(';')[0]
            if item.find('购方开户银行') != -1:
                if '：' in item.split('购方开户银行')[1]:
                    self.data.loc['购方开户行及账号'] = item.split('购方开户银行：')[1].split(';')[0] + item.split('银行账号：')[1].split(';')[0]
                else:
                    self.data.loc['购方开户行及账号'] = item.split('购方开户银行:')[1].split(';')[0] + item.split('银行账号:')[1].split(';')[0]
        self.data.loc['备注']=''



    def data_clean_zzs_place(self):
        # i. 无效ASCII·字符清除
        self.data.columns = ['Details']
        self.data['Details'] = self.data['Details'].str.replace('\n', '')
        #ii.重复定位数据清除
        for item in self.data['Details']:
            if '￥' in item:
                index = item.index('￥')
                cleaned = item[index+1:]
                self.data['Details'] = self.data['Details'].replace(item, cleaned)
                print("Repeated opeartor cleaned once.")
        for item in self.data['Details']:
            if '%' in item:
                index = item.index('%')
                cleaned = item[index+1:]
                self.data['Details'] = self.data['Details'].replace(item, cleaned)
                print("Repeated data cleaned once.")


    def Clean_Single_invoice(self):
        type = self._check_type()
        if type == 1:
            print("该发票类型为==电子发票（普通发票)==")
            self.data_clean_normal()
            print("==数据清洗完成==")
        elif type == 2:
            print("该发票类型为==电⼦发票（增值税专用发票)==")
            self.data_clean_zzs_normal()
            print("==数据清洗完成==")
        elif type == 3:
            print("该发票类型为==上海增值税电子普通发票==")
            self.data_clean_zzs_place()
            print("==数据清洗完成==")
        else:
            print("Unknown type of invoice, please check it manually.")
        return self.data