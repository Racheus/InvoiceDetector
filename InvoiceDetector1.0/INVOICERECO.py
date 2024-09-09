import os
import re
import pandas as pd
import pdfplumber as pb
import numpy as np
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from InvoiceDetector import InvoiceDetector
from PIL import Image, ImageTk, ImageEnhance
import threading    

class Extractor(object):
    def __init__(self, path):
        self.file = path if os.path.isfile else None

    def _load_data(self):
        if self.file and os.path.splitext(self.file)[1] == '.pdf':
            pdf = pb.open(self.file)
            page = pdf.pages[0]
            words = page.extract_words(x_tolerance=5)
            lines = page.lines
            # convert coordination
            for index, word in enumerate(words):
                words[index]['y0'] = word['top']
                words[index]['y1'] = word['bottom']
            for index, line in enumerate(lines):
                lines[index]['x1'] = line['x0']+line['width']
                lines[index]['y0'] = line['top']
                lines[index]['y1'] = line['bottom']
            return {'words': words, 'lines': lines}
        else:
            print("file %s cann't be opened." % self.file)
            return None

    def _fill_line(self, lines):
        hlines = [line for line in lines if line['width'] > 0]  # 筛选横线
        hlines = sorted(hlines, key=lambda h: h['width'], reverse=True)[:-2]  # 剔除较短的两根
        vlines = [line for line in lines if line['height'] > 0]  # 筛选竖线
        vlines = sorted(vlines, key=lambda v: v['y0'])  # 按照坐标排列
        # 查找边框顶点
        hx0 = hlines[0]['x0']  # 左侧
        hx1 = hlines[0]['x1']  # 右侧
        vy0 = vlines[0]['y0']  # 顶部
        vy1 = vlines[-1]['y1']  # 底部

        thline = {'x0': hx0, 'y0': vy0, 'x1': hx1, 'y1': vy0}  # 顶部横线
        bhline = {'x0': hx0, 'y0': vy1, 'x1': hx1, 'y1': vy1}  # 底部横线
        lvline = {'x0': hx0, 'y0': vy0, 'x1': hx0, 'y1': vy1}  # 左侧竖线
        rvline = {'x0': hx1, 'y0': vy0, 'x1': hx1, 'y1': vy1}  # 右侧竖线

        hlines.insert(0, thline)
        hlines.append(bhline)
        vlines.insert(0, lvline)
        vlines.append(rvline)
        return {'hlines': hlines, 'vlines': vlines}

    def _is_point_in_rect(self, point, rect):
        '''判断点是否在矩形内'''
        px, py = point
        p1, p2, p3, p4 = rect
        if p1[0] <= px <= p2[0] and p1[1] <= py <= p3[1]:
            return True
        else:
            return False

    def _find_cross_points(self, hlines, vlines):
        points = []
        delta = 1
        for vline in vlines:
            vx0 = vline['x0']
            vy0 = vline['y0']
            vy1 = vline['y1']
            for hline in hlines:
                hx0 = hline['x0']
                hy0 = hline['y0']
                hx1 = hline['x1']
                if (hx0-delta) <= vx0 <= (hx1+delta) and (vy0-delta) <= hy0 <= (vy1+delta):
                    points.append((int(vx0), int(hy0)))
        return points

    def _find_rects(self, cross_points):
        # 构造矩阵
        X = sorted(set([int(p[0]) for p in cross_points]))
        Y = sorted(set([int(p[1]) for p in cross_points]))
        df = pd.DataFrame(index=Y, columns=X)
        for p in cross_points:
            x, y = int(p[0]), int(p[1])
            df.loc[y, x] = 1
        df = df.fillna(0)
        # 寻找矩形
        rects = []
        COLS = len(df.columns)-1
        ROWS = len(df.index)-1
        for row in range(ROWS):
            for col in range(COLS):
                p0 = df.iat[row, col]  # 主点：必能构造一个矩阵
                cnt = col+1
                while cnt <= COLS:
                    p1 = df.iat[row, cnt]
                    p2 = df.iat[row+1, col]
                    p3 = df.iat[row+1, cnt]
                    if p0 and p1 and p2 and p3:
                        rects.append(((df.columns[col], df.index[row]), (df.columns[cnt], df.index[row]), (
                            df.columns[col], df.index[row+1]), (df.columns[cnt], df.index[row+1])))
                        break
                    else:
                        cnt += 1
        return rects

    def _put_words_into_rect(self, words, rects):
        # 将words按照坐标层级放入矩阵中
        groups = {}
        delta = 2
        for word in words:
            p = (int(word['x0']), int((word['y0']+word['y1'])/2))
            flag = False
            for r in rects:
                if self._is_point_in_rect(p, r):
                    flag = True
                    groups[('IN', r[0][1], r)] = groups.get(
                        ('IN', r[0][1], r), [])+[word]
                    break
            if not flag:
                y_range = [
                    p[1]+x for x in range(delta)]+[p[1]-x for x in range(delta)]
                out_ys = [k[1] for k in list(groups.keys()) if k[0] == 'OUT']
                flag = False
                for y in set(y_range):
                    if y in out_ys:
                        v = out_ys[out_ys.index(y)]
                        groups[('OUT', v)].append(word)
                        flag = True
                        break
                if not flag:
                    groups[('OUT', p[1])] = [word]
        return groups

    def _find_text_by_same_line(self, group, delta=1):
        words = {}
        group = sorted(group, key=lambda x: x['x0'])
        for w in group:
            bottom = int(w['bottom'])
            text = w['text']
            k1 = [bottom-i for i in range(delta)]
            k2 = [bottom+i for i in range(delta)]
            k = set(k1+k2)
            flag = False
            for kk in k:
                if kk in words:
                    words[kk] = words.get(kk, '')+text
                    flag = True
                    break
            if not flag:
                words[bottom] = words.get(bottom, '')+text
        return words

    def _split_words_into_diff_line(self, groups):
        groups2 = {}
        for k, g in groups.items():
            words = self._find_text_by_same_line(g, 3)
            groups2[k] = words
        return groups2

    def _index_of_y(self, x, rects):
        for index, r in enumerate(rects):
            if x == r[2][0][0]:
                return index+1 if index+1 < len(rects) else None
        return None

    def _find_outer(self, k, words):
        df = pd.DataFrame()
        for pos, text in words.items():
            if re.search(r'发票$', text):  # 发票名称
                df.loc[0, '发票名称'] = text
            elif re.search(r'发票代码', text):  # 发票代码
                num = ''.join(re.findall(r'[0-9]+', text))
                df.loc[0, '发票代码'] = num
            elif re.search(r'发票号码', text):  # 发票号码
                num = ''.join(re.findall(r'[0-9]+', text))
                df.loc[0, '发票号码'] = num
            elif re.search(r'开票日期', text):  # 开票日期
                date = ''.join(re.findall(
                    r'[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日', text))
                df.loc[0, '开票日期'] = date
            elif '机器编号' in text and '校验码' in text:  # 校验码
                text1 = re.search(r'校验码:\d+', text)[0]
                num = ''.join(re.findall(r'[0-9]+', text1))
                df.loc[0, '校验码'] = num
                text2 = re.search(r'机器编号:\d+', text)[0]
                num = ''.join(re.findall(r'[0-9]+', text2))
                df.loc[0, '机器编号'] = num
            elif '机器编号' in text:
                num = ''.join(re.findall(r'[0-9]+', text))
                df.loc[0, '机器编号'] = num
            elif '校验码' in text:
                num = ''.join(re.findall(r'[0-9]+', text))
                df.loc[0, '校验码'] = num
            elif re.search(r'收款人', text):
                items = re.split(r'收款人:|复核:|开票人:|销售方:', text)
                items = [item for item in items if re.sub(
                    r'\s+', '', item) != '']
                df.loc[0, '收款人'] = items[0] if items and len(items) > 0 else ''
                df.loc[0, '复核'] = items[1] if items and len(items) > 1 else ''
                df.loc[0, '开票人'] = items[2] if items and len(items) > 2 else ''
                df.loc[0, '销售方'] = items[3] if items and len(items) > 3 else ''
        return df

    def _find_and_sort_rect_in_same_line(self, y, groups):
        same_rects_k = [k for k, v in groups.items() if k[1] == y]
        return sorted(same_rects_k, key=lambda x: x[2][0][0])

    def _find_inner(self, k, words, groups, groups2, free_zone_flag=False):
        df = pd.DataFrame()
        sort_words = sorted(words.items(), key=lambda x: x[0])
        text = [word for k, word in sort_words]
        context = ''.join(text)
        if '购买方' in context or '销售方' in context:
            y = k[1]
            x = k[2][0][0]
            same_rects_k = self._find_and_sort_rect_in_same_line(y, groups)
            target_index = self._index_of_y(x, same_rects_k)
            print(target_index)
            if target_index is not None:
                 target_k = same_rects_k[target_index]
            else:
                return df, free_zone_flag
            group_context = groups2[target_k]
            prefix = '购买方' if '购买方' in context else '销售方'
            for pos, text in group_context.items():
                if '名称' in text:
                    name = re.sub(r'名称:', '', text)
                    df.loc[0, prefix+'名称'] = name
                elif '纳税人识别号' in text:
                    tax_man_id = re.sub(r'纳税人识别号:', '', text)
                    df.loc[0, prefix+'纳税人识别号'] = tax_man_id
                elif '地址、电话' in text:
                    addr = re.sub(r'地址、电话:', '', text)
                    df.loc[0, prefix+'地址电话'] = addr
                elif '开户行及账号' in text:
                    account = re.sub(r'开户行及账号:', '', text)
                    df.loc[0, prefix+'开户行及账号'] = account
        elif '密码区' in context:
            y = k[1]
            x = k[2][0][0]
            same_rects_k = self._find_and_sort_rect_in_same_line(y, groups)
            target_index = self._index_of_y(x, same_rects_k)
            target_k = same_rects_k[target_index]
            words = groups2[target_k]
            context = [v for k, v in words.items()]
            context = ''.join(context)
            df.loc[0, '密码区'] = context
        elif '价税合计' in context:
            y = k[1]
            x = k[2][0][0]
            same_rects_k = self._find_and_sort_rect_in_same_line(y, groups)
            target_index = self._index_of_y(x, same_rects_k)
            target_k = same_rects_k[target_index]
            group_words = groups2[target_k]
            group_context = ''.join([w for k, w in group_words.items()])
            items = re.split(r'[(（]小写[)）]', group_context)
            b = items[0] if items and len(items) > 0 else ''
            s = items[1] if items and len(items) > 1 else ''
            df.loc[0, '价税合计(大写)'] = b
            df.loc[0, '价税合计(小写)'] = s
        elif '备注' in context:
            y = k[1]
            x = k[2][0][0]
            same_rects_k = self._find_and_sort_rect_in_same_line(y, groups)
            target_index = self._index_of_y(x, same_rects_k)
            if target_index:
                target_k = same_rects_k[target_index]
                group_words = groups2[target_k]
                group_context = ''.join([w for k, w in group_words.items()])
                df.loc[0, '备注'] = group_context
            else:
                df.loc[0, '备注'] = ''
        else:
            if free_zone_flag:
                return df, free_zone_flag
            y = k[1]
            x = k[2][0][0]
            same_rects_k = self._find_and_sort_rect_in_same_line(y, groups)
            if len(same_rects_k) == 8:
                free_zone_flag = True
                for kk in same_rects_k:
                    yy = kk[1]
                    xx = kk[2][0][0]
                    words = groups2[kk]
                    words = sorted(words.items(), key=lambda x: x[0]) if words and len(
                        words) > 0 else None
                    key = words[0][1] if words and len(words) > 0 else None
                    val = [word[1] for word in words[1:]
                           ] if key and words and len(words) > 1 else ''
                    val = '\n'.join(val) if val else ''
                    if key:
                        df.loc[0, key] = val
        return df, free_zone_flag

    def extract(self):
        data = self._load_data()
        words = data['words']
        lines = data['lines']

        lines = self._fill_line(lines)
        hlines = lines['hlines']
        vlines = lines['vlines']

        cross_points = self._find_cross_points(hlines, vlines)
        rects = self._find_rects(cross_points)

        word_groups = self._put_words_into_rect(words, rects)
        word_groups2 = self._split_words_into_diff_line(word_groups)

        df = pd.DataFrame()
        free_zone_flag = False
        for k, words in word_groups2.items():
            if k[0] == 'OUT':
                df_item = self._find_outer(k, words)
            else:
                df_item, free_zone_flag = self._find_inner(
                    k, words, word_groups, word_groups2, free_zone_flag)
            df = pd.concat([df, df_item], axis=1)
        return df

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

    def Save(self,dest):
        self.InvoiceList.to_excel(dest)
        print("Data Saved! -- path: " + str(dest))

    def Showinfo(self):
        print("Welcome to use InvoiceDetector(Version 1.0)")
        print(f"Valid Invoice Count: {self.valid_count-1}")
        print(f"Error Invoice Count: {len(self.ErrorList)}, Please check them manually")
        return self.valid_count-1, len(self.ErrorList), self.ErrorList


root = tk.Tk()
root.geometry("800x730")
root.title("Invoice Detector")
folder_path = ""
output_path = ""
user_input = ""
# 初始化CustomTkinter
ctk.set_appearance_mode("dark")  # 可选: "light", "dark"
ctk.set_default_color_theme("dark-blue")  # 可选: "blue", "green", "dark-blue"

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Selected file: {file_path}")

def select_folder():
    global output_path
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        print(f"Selected folder: {folder_path}")
    output_path.configure(text=f"Selected folder: {folder_path}")
    

def get_input ():
    global user_input
    user_input = input_entry.get()
    result_label.configure(text=f"Your invoice data has been saved in: {user_input}.xlsx")

def run_detector():
    global valid_count, error_count, error_list
    detector = InvoiceDetector(folder_path)
    detector.Detect()
    detector.Clean()
    detector.Check_Error_List()
    detector.Save(f'{user_input}.xlsx')
    valid_count, error_count, error_list = detector.Showinfo()
    run_result_label.configure(text=f"Valid Invoice Count: {valid_count}\nError Invoice Count: {error_count}\nError List: {error_list}")
    progressbar.stop()

def start_detector():
    threading.Thread(target=run_detector).start()
file_title = ctk.CTkLabel(master=root, text="Invoice Detector(Version 1.0)",text_color="Black",font=("Consolas", 30))
file_title.pack(pady=10)


if __name__ == "__main__":
    file_label = ctk.CTkLabel(master=root, text="Please select a file to upload:",text_color="blue")
    file_label.pack(pady=10)

    upload_button = ctk.CTkButton(master=root, text="Upload File", command=upload_file)
    upload_button.pack(pady=10)



    folder_button = ctk.CTkButton(master=root, text="Select Folder", command=select_folder)
    folder_button.pack(pady=10)


    output_path = ctk.CTkLabel(master=root, text="",text_color="red")
    output_path.pack(pady=10)

    input_label = ctk.CTkLabel(master=root, text="Please name your Excel file: ",text_color="blue")
    input_label.pack(pady=5)

    input_entry = ctk.CTkEntry(master=root, width=300)
    input_entry.pack(pady=5) 

    submit_button = ctk.CTkButton(master=root, text="Submit", command=get_input)
    submit_button.pack(pady=5)

    progressbar = ctk.CTkProgressBar(master=root, mode='indeterminate')
    progressbar.start()
    progressbar.pack(pady=10)

    run_button = ctk.CTkButton(master=root, text="Run Detector", command=run_detector)
    run_button.pack(pady=5)

    # 显示结果的标签
    result_label = ctk.CTkLabel(master=root, text="",text_color="red")
    result_label.pack(pady=10)

    run_result_label = ctk.CTkLabel(master=root, text="",text_color="red")
    run_result_label.pack(pady=10)


    # 加载背景图片
    bg_image = Image.open("background.jpg")
    bg_image = bg_image.resize((800, 200))  
    alpha = 0.7 
    bg_image = ImageEnhance.Brightness(bg_image).enhance(alpha)
    bg_image = ImageTk.PhotoImage(bg_image)
    # 创建Canvas并设置背景图片
    canvas = tk.Canvas(root, width=800, height=200, bd=0, highlightthickness=0)
    canvas.pack(padx=0, pady=0)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    frame = ctk.CTkFrame(canvas, bg_color="white", width=400, height=100)
    frame.place(relx=0.5, rely=0.5, anchor="center")


    image = Image.open("logo.png")
    image = image.resize((80, 35))
    photo = ImageTk.PhotoImage(image)
    image_label = ctk.CTkLabel(master=frame, image=photo, text="")
    image_label.pack(pady=10)

    AUTHOR_label = ctk.CTkLabel(master=frame, text="Author: Racheus Zhao, JAKA Intern \n Copyright©2024,All rights served.",text_color="gray")
    AUTHOR_label.pack(pady=0)

    root.mainloop()