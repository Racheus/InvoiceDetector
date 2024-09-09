import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from InvoiceDetector import InvoiceDetector
from tkcalendar import DateEntry
from PIL import Image, ImageTk, ImageEnhance
from InvoiceManager import InvoiceManager
import threading    
# 创建主窗口
root = tk.Tk()
root.geometry("800x730")
root.title("Invoice Detector")
folder_path = ""
output_path = ""
user_input = ""
# 初始化CustomTkinter
ctk.set_appearance_mode("light")  # 可选: "light", "dark"
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
        input_label.place(x=130, y=10)
        input_entry.place(x=50, y=35)
        submit_button.place(x=130, y=70)
    output_path.configure(text=f"Selected folder: {folder_path}")
    

def get_input ():
    global user_input
    user_input = input_entry.get()
    result_label.configure(text=f"Your invoice data has been saved in: {user_input}.xlsx")
    result_label.place(x=50, y=100)

def run_detector():
    global detector
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

def get_date(cal,date_label):
    selected_date = cal.get_date()
    print(f"Selected Date: {selected_date}")
    date_label.configure(text=f"Selected Date: {selected_date}")

def open_add_window():
    new_window = ctk.CTkToplevel(root)
    new_window.geometry("800x450")
    new_window.title("Add New Invoice")

    add_windoe_title = ctk.CTkLabel(master=new_window, text="Add New Invoice",text_color="Black",font=("Consolas", 30))
    add_windoe_title.pack(pady=10)

    new_invoice_code_frame = ctk.CTkFrame(master=new_window, bg_color="white", width=750, height=320)
    new_invoice_code_frame.place(x=20 , y=50)
    new_invoice_code_label = ctk.CTkLabel(master=new_invoice_code_frame, text="发票号码: (eg.92510181MA7XXXXX)",text_color="blue")
    new_invoice_code_label.place(x=10, y=5)
    new_invoice_code_entry = ctk.CTkEntry(master=new_invoice_code_frame, width=300)
    new_invoice_code_entry.place(x=10, y=30)

    new_invoice_date_label = ctk.CTkLabel(master=new_invoice_code_frame, text="开票日期: ",text_color="blue")
    new_invoice_date_label.place(x=350 , y=5)
    cal = DateEntry(new_invoice_code_frame, width=12, borderwidth=2,                          
                        background = "green",
                        foreground = "white",
                        selectbackground = "blue", 
                        normalbackground = "lightgreen",
                        weekendbackground = "darkgreen",
                        weekendforeground = "white")
    cal.place(x=350, y=30)
    date_button = ctk.CTkButton(master=new_invoice_code_frame, text="Confirm", width = 50,command=lambda: get_date(cal, date_label))
    date_button.place(x=480, y=30)
    global date_label
    date_label = ctk.CTkLabel(master=new_invoice_code_frame, text="")
    date_label.place(x=560, y=30)

    new_buyer_code_label = ctk.CTkLabel(master=new_invoice_code_frame, text="购买方纳税人识别号: (eg.91310115MA1XXXXX)",text_color="blue")
    new_buyer_code_label.place(x=10, y=60)
    new_buyer_code_entry = ctk.CTkEntry(master=new_invoice_code_frame, width=300)
    new_buyer_code_entry.place(x=10, y=85)

    new_buyer_name_label = ctk.CTkLabel(master=new_invoice_code_frame, text="购买方名称: ",text_color="blue")
    new_buyer_name_label.place(x=350, y=60)
    new_buyer_name_entry = ctk.CTkEntry(master=new_invoice_code_frame, width=300)
    new_buyer_name_entry.place(x=350, y=85)

    new_seller_code_label = ctk.CTkLabel(master=new_invoice_code_frame, text="销售方纳税人识别号: (eg.91310115MA1XXXXX)",text_color="blue")
    new_seller_code_label.place(x=10, y=115)
    new_seller_code_entry = ctk.CTkEntry(master=new_invoice_code_frame, width=300)
    new_seller_code_entry.place(x=10, y=140)

    new_seller_name_label = ctk.CTkLabel(master=new_invoice_code_frame, text="销售方名称: ",text_color="blue")
    new_seller_name_label.place(x=350, y=115)
    new_seller_name_entry = ctk.CTkEntry(master=new_invoice_code_frame, width=300)
    new_seller_name_entry.place(x=350, y=140)

    new_invoice_amount_SMALL_label = ctk.CTkLabel(master=new_invoice_code_frame, text="价税合计(小写): ",text_color="blue")
    new_invoice_amount_SMALL_label.place(x=10, y=170)
    new_invoice_amount_SMALL_entry = ctk.CTkEntry(master=new_invoice_code_frame, width=300)
    new_invoice_amount_SMALL_entry.place(x=10, y=195)

    note_label = ctk.CTkLabel(master=new_invoice_code_frame, text="备注: ",text_color="blue")
    note_label.place(x=10, y=225)
    note_entry = ctk.CTkTextbox(master=new_invoice_code_frame, width=300, height=60)
    note_entry.place(x=10, y=250)


    new_submit_button = ctk.CTkButton(master=new_window, text="Submit", command=lambda: submit_new_entry(new_invoice_code_entry.get(), cal.get_date(), new_buyer_code_entry.get(), new_buyer_name_entry.get(), new_seller_code_entry.get(), new_seller_name_entry.get(), new_invoice_amount_SMALL_entry.get(), note_entry.get("1.0", "end-1c")))
    new_submit_button.place(x=250, y=390)

    new_cancel_button = ctk.CTkButton(master=new_window, text="Cancel", command=new_window.destroy)
    new_cancel_button.place(x=400, y=390)

def submit_new_entry(invoice_code, invoice_date, buyer_code, buyer_name, seller_code, seller_name, invoice_amount_SMALL, note):
    new_invoice = InvoiceManager()
    new_invoice.get_info(invoice_code, invoice_date, buyer_code, buyer_name, seller_code, seller_name, invoice_amount_SMALL, note)
    print(f"New Invoice: {new_invoice.invoice_code}, {new_invoice.invoice_date}, {new_invoice.buyer_code}, {new_invoice.buyer_name}, {new_invoice.seller_code}, {new_invoice.seller_name}, {new_invoice.invoice_amount_SMALL}, {new_invoice.note}")
    detector.Add(new_invoice.data)
    detector.Save(f'{user_input}.xlsx')
    valid_count, error_count, error_list = detector.Showinfo()
    run_result_label.configure(text=f"Valid Invoice Count: {valid_count}\nError Invoice Count: {error_count}\nError List: {error_list}")
    


file_title = ctk.CTkLabel(master=root, text="Invoice Detector(Version 1.1)",text_color="Black",font=("Consolas", 30))
file_title.pack(pady=10)

select_frame = ctk.CTkFrame(master=root, bg_color="white", width=400, height=100)
select_frame.pack(pady=10)

file_label = ctk.CTkLabel(master=select_frame, text="Please select a file to upload:",text_color="blue")
file_label.place(x = 130, y = 10)

upload_button = ctk.CTkButton(master=select_frame, text="Upload File", command=upload_file)
upload_button.place(x = 50, y = 50)

folder_button = ctk.CTkButton(master=select_frame, text="Select Folder", command=select_folder)
folder_button.place(x = 230, y = 50)

output_path = ctk.CTkLabel(master=root, text="",text_color="red")
output_path.pack(pady=2)

input_frame = ctk.CTkFrame(master=root, bg_color="white", width=400, height=130)
input_frame.pack(pady=10)

input_label = ctk.CTkLabel(master=input_frame, text="Please name your Excel file: ",text_color="blue")

input_entry = ctk.CTkEntry(master=input_frame, width=300)

submit_button = ctk.CTkButton(master=input_frame, text="Submit", command=get_input)

progressbar = ctk.CTkProgressBar(master=root, mode='indeterminate')
progressbar.start()
progressbar.pack(pady=10)

run_button = ctk.CTkButton(master=root, text="Run Detector", command=run_detector)
run_button.pack(pady=5)

# 显示结果的标签
result_label = ctk.CTkLabel(master=input_frame, text="",text_color="red")


run_result_label = ctk.CTkLabel(master=root, text="",text_color="red")
run_result_label.pack(pady=10)

open_window_button = ctk.CTkButton(master=root, text="Create new invoice", command=open_add_window)
open_window_button.pack(pady=20)


# 加载背景图片
bg_image = Image.open("background.jpg")
bg_image = bg_image.resize((800, 200), Image.Resampling.LANCZOS)
alpha = 0.7 
bg_image = ImageEnhance.Brightness(bg_image).enhance(alpha)
bg_image = ImageTk.PhotoImage(bg_image)
# 创建Canvas并设置背景图片
canvas = tk.Canvas(root, width=800, height=200, bd=0, highlightthickness=0)
canvas.pack(padx=0, pady=0)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

frame = ctk.CTkFrame(canvas, bg_color="white", width=400, height=50)
frame.place(relx=0.5, rely=0.5, anchor="center")


image = Image.open("logo.png")
photo = ctk.CTkImage(image)
image_label = ctk.CTkLabel(master=frame, image=photo, text="")
image_label.pack(pady=10)

AUTHOR_label = ctk.CTkLabel(master=frame, text="Author: Racheus Zhao,Shuo Qi,JAKA Intern \n Copyright ©2024,All rights served.",text_color="gray")
AUTHOR_label.pack(pady=0)

root.mainloop()