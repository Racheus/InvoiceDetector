import pandas as pd
import customtkinter as ctk
import tkinter as tk

class InvoiceManager:
    def __init__(self):
        self.data = pd.DataFrame()
        self.invoice_code = ""  # 发票号码
        self.invoice_date = ""  # 开票日期
        self.buyer_code = ""  # 购买方纳税人识别号
        self.buyer_name = ""  # 购买方名称
        self.seller_code = "" # 销售方纳税人识别号
        self.seller_name = "" # 销售方名称
        self.invoice_amount_SMALL = ""  # 价税合计（小写）
        self.note = ""  # 备注
    
    def get_info(self, invoice_code, invoice_date, buyer_code, buyer_name, seller_code, seller_name, invoice_amount_SMALL, note):
        self.invoice_code = invoice_code
        self.invoice_date = invoice_date
        self.buyer_code = buyer_code
        self.buyer_name = buyer_name
        self.seller_code = seller_code
        self.seller_name = seller_name
        self.invoice_amount_SMALL = invoice_amount_SMALL
        self.note = note
        self.data = pd.DataFrame({
            '发票号码': str(self.invoice_code),
            '开票日期': str(self.invoice_date),
            '购买方纳税人识别号': str(self.buyer_code),
            '购买方名称': str(self.buyer_name),
            '销售方纳税人识别号': str(self.seller_code),
            '销售方名称': str(self.seller_name),
            '价税合计(小写)': str(self.invoice_amount_SMALL),
            '备注': str(self.note)
        }, index=[0])

    

        

