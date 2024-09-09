import sys
import Ui_test
import time
import pymysql
from sqlalchemy import create_engine
from PyQt6 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
import Ui_name,Ui_errorlist, Ui_success , Ui_add ,Ui_modify,Ui_delete, Ui_login
from InvoiceDetector import InvoiceDetector
from InvoiceManager import InvoiceManager
class HelpWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.help_window = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('帮助文档')
        self.resize(1200, 900)
        widget = QtWebEngineWidgets.QWebEngineView(self)
        widget.move(0, 0)
        widget.resize(1200, 900)
        widget.load(QtCore.QUrl("https://app.gitbook.com/o/1PfFr7ZU8J7JISs4XM51/s/rvJFj9VuFQCR0yIUwz32/"))

def open_help_web():
    ui.help_window = HelpWindow()
    ui.help_window.show()

def browse_file():
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName()
    if file_path:
        print(f"Selected file: {file_path}")
        ui.textBrowser.setText(f"已选择: {file_path}")

def browse_folder():
    global folder_path 
    folder_path = QtWidgets.QFileDialog.getExistingDirectory()
    if folder_path:
        print(f"Selected folder: {folder_path}")
        ui.textBrowser.setText(f"已选择: {folder_path}")

def get_account_and_password():
    global user_name, user_password
    ui_login = Ui_login.Ui_Login()
    login_Dialog = QtWidgets.QDialog()
    login_Dialog.setWindowTitle("Login")
    ui_login.setupUi(login_Dialog)
    login_Dialog.show()
    if login_Dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        user_name = ui_login.lineEdit_account.text()
        user_password = ui_login.lineEdit_password.text()
        print(f"User Name: {user_name}, Password: {user_password}")

def run_detector():
    global detector
    global user_input
    global valid_count, error_count, error_list
    ui_name = Ui_name.Ui_Dialog()
    name_Dialog = QtWidgets.QDialog()
    name_Dialog.setWindowTitle("Name Reminder")
    ui_name.setupUi(name_Dialog)
    name_Dialog.show()
    ui.progressBar.setRange(0,10)
    if name_Dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        user_input = ui_name.lineEdit.text()
        print(f"User input: {user_input}")
        detector = InvoiceDetector(folder_path)
        ui.progressBar.setValue(3)
    detector.Detect()
    ui.progressBar.setValue(5)
    detector.Clean()
    time.sleep(0.5)
    ui.progressBar.setValue(7)
    detector.Check_Error_List()
    ui.progressBar.setValue(9)
    detector.Save(f'{user_input}.xlsx')
    valid_count, error_count, error_list = detector.Showinfo(user_name, user_password)
    ui.result_label.setText(f"Detect Successfully!\nValid Invoice Count: {valid_count}\nError Invoice Count: {error_count}\n")
    if error_count > 0:
        ui_errorlist = Ui_errorlist.Ui_ErrorList()
        error_Dialog = QtWidgets.QDialog()
        error_Dialog.setWindowTitle("Error Reminder")
        ui_errorlist.setupUi(error_Dialog)
        ui_errorlist.textBrowser.setText(str(error_list))
        error_Dialog.show()
        if ui_errorlist.pushButton.clicked.connect(lambda: ui_errorlist.pushButton.clicked):
            ui_errorlist.pushButton.clicked.connect(add_invoice)
        error_Dialog.exec()
    else:
        ui_success = Ui_success.Ui_Success()
        success_Dialog = QtWidgets.QDialog()
        success_Dialog.setWindowTitle("Success Reminder")
        ui_success.setupUi(success_Dialog)
        success_Dialog.show()
        success_Dialog.exec()
    ui.progressBar.setValue(10)
    del_repeat_invoice()
    


def Search_button_clicked():
    global invoice_code_user_input
    invoice_code_user_input = ui.lineEdit.text()
    Search_Invoice()

def Search_Invoice():
    db = pymysql.connect(
        host="localhost",
        user=user_name,
        password=user_password,
        database="db_Invoice")
    cursor = db.cursor()
    sql = f"SELECT * FROM tb_invoice WHERE invoice_code = '{invoice_code_user_input}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        ui.textBrowser_invoice_info.setText("The invoice has been searched successfully!")
        ui.textBrowser_invoicecode.setText(f"{result[0][1]}")
        ui.textBrowser_date.setText(f"{result[0][2]}")
        ui.textBrowser_buyercode.setText(f"{result[0][3]}")
        ui.textBrowser_buyername.setText(f"{result[0][4]}")
        ui.textBrowser_sellercode.setText(f"{result[0][5]}")
        ui.textBrowser_sellername.setText(f"{result[0][6]}")
        ui.textBrowser_totalprice.setText(f"{result[0][7]}")
        ui.textBrowser_notes.setText(f"{result[0][8]}")
    else:
        ui.textBrowser_invoice_info.setText("The invoice has not found!")
        ui.textBrowser_invoicecode.setText("N")
        ui.textBrowser_date.setText("O")
        ui.textBrowser_buyercode.setText("F")
        ui.textBrowser_buyername.setText("T")
        ui.textBrowser_sellercode.setText("U")
        ui.textBrowser_sellername.setText("O")
        ui.textBrowser_totalprice.setText("N")
        ui.textBrowser_notes.setText("D \n 感谢您的使用和支持！")                  
    db.close()
    

def add_invoice():
    ui_add = Ui_add.Ui_Dialog()
    add_Dialog = QtWidgets.QDialog()
    add_Dialog.setWindowTitle("Add New Invoice")
    ui_add.setupUi(add_Dialog)
    add_Dialog.show()
    if add_Dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        new_invoice_code = ui_add.textEdit_code_add.toPlainText()
        new_invoice_date = ui_add.dateEdit.date().toString(QtCore.Qt.DateFormat.ISODate)
        new_buyer_code = ui_add.textEdit_buyercode_add.toPlainText()
        new_buyer_name = ui_add.textEdit__buyername_add.toPlainText()
        new_seller_code = ui_add.textEdit_sellercode_add.toPlainText()
        new_seller_name = ui_add.textEdit_sellername_add.toPlainText()
        new_invoice_amount_SMALL = ui_add.textEdit_totalprice_add.toPlainText()
        new_note = ui_add.textEdit_note_add.toPlainText()
        new_invoice = InvoiceManager()
        new_invoice.get_info(new_invoice_code, new_invoice_date, new_buyer_code, new_buyer_name, new_seller_code, new_seller_name, new_invoice_amount_SMALL, new_note)
        print(f"New Invoice: {new_invoice.invoice_code}, {new_invoice.invoice_date}, {new_invoice.buyer_code}, {new_invoice.buyer_name}, {new_invoice.seller_code}, {new_invoice.seller_name}, {new_invoice.invoice_amount_SMALL}, {new_invoice.note}")
        db = pymysql.connect(
            host="localhost",
            user=user_name,
            password=user_password,
            database="db_Invoice")
        cursor = db.cursor()
        cursor.execute("USE db_Invoice;")
        sql = """INSERT INTO tb_invoice(invoice_code, date, buyer_code, buyer_name, seller_code, seller_name, invoice_amount_SMALL, note) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (new_invoice.invoice_code, new_invoice.invoice_date, new_invoice.buyer_code, new_invoice.buyer_name, new_invoice.seller_code, new_invoice.seller_name, new_invoice.invoice_amount_SMALL, new_invoice.note))
        db.commit()
        db.close()
    

def modify_invoice():
    ui_modify = Ui_modify.Ui_Dialog()
    modify_Dialog = QtWidgets.QDialog()
    modify_Dialog.setWindowTitle("Modify Invoice")
    ui_modify.setupUi(modify_Dialog)
    db = pymysql.connect(
        host="localhost",
        user=user_name,
        password=user_password,
        database="db_Invoice")
    cursor = db.cursor()
    sql_search = f"SELECT * FROM tb_invoice WHERE invoice_code = '{invoice_code_user_input}'"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    ui_modify.textEdit_code_mod.setText(f"{result[0][1]}")
    ui_modify.dateEdit.setDate(QtCore.QDate.fromString(result[0][2], QtCore.Qt.DateFormat.ISODate))
    ui_modify.textEdit_buyercode_mod.setText(f"{result[0][3]}")
    ui_modify.textEdit__buyername_mod.setText(f"{result[0][4]}")
    ui_modify.textEdit_sellercode_mod.setText(f"{result[0][5]}")
    ui_modify.textEdit_sellername_mod.setText(f"{result[0][6]}")
    ui_modify.textEdit_totalprice_add.setText(f"{result[0][7]}")
    ui_modify.textEdit_note_mod.setText(f"{result[0][8]}")
    modify_Dialog.show()
    if modify_Dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        modify_invoice_code = ui_modify.textEdit_code_mod.toPlainText()
        modify_invoice_date = ui_modify.dateEdit.date().toString(QtCore.Qt.DateFormat.ISODate)
        modify_buyer_code = ui_modify.textEdit_buyercode_mod.toPlainText()
        modify_buyer_name = ui_modify.textEdit__buyername_mod.toPlainText()
        modify_seller_code = ui_modify.textEdit_sellercode_mod.toPlainText()
        modify_seller_name = ui_modify.textEdit_sellername_mod.toPlainText()
        modify_invoice_amount_SMALL = ui_modify.textEdit_totalprice_add.toPlainText()
        modify_note = ui_modify.textEdit_note_mod.toPlainText()
        db = pymysql.connect(
            host="localhost",
            user=user_name,
            password=user_password,
            database="db_Invoice")
        cursor = db.cursor()
        cursor.execute("USE db_Invoice;")
        sql = f"""UPDATE tb_invoice SET date = '{modify_invoice_date}', buyer_code = '{modify_buyer_code}', buyer_name = '{modify_buyer_name}', seller_code = '{modify_seller_code}', seller_name = '{modify_seller_name}', invoice_amount_SMALL = '{modify_invoice_amount_SMALL}', note = '{modify_note}' WHERE invoice_code = '{modify_invoice_code}'"""
        cursor.execute(sql)
        db.commit()
        db.close()
        print(f"Modify Invoice: {modify_invoice_code}, {modify_invoice_date}, {modify_buyer_code}, {modify_buyer_name}, {modify_seller_code}, {modify_seller_name}, {modify_invoice_amount_SMALL}, {modify_note}")
    

def delete_invoice():
    ui_delete = Ui_delete.Ui_Dialog()
    delete_Dialog = QtWidgets.QDialog()
    delete_Dialog.setWindowTitle("Delete Invoice")
    ui_delete.setupUi(delete_Dialog)
    if delete_Dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        db = pymysql.connect(
            host="localhost",
            user=user_name,
            password=user_password,
            database="db_Invoice")
        cursor = db.cursor()
        sql = f"DELETE FROM tb_invoice WHERE invoice_code = '{invoice_code_user_input}'"
        cursor.execute(sql)
        db.commit()
        db.close()
    

def del_repeat_invoice():
    db = pymysql.connect(
        host="localhost",
        user= user_name,
        password= user_password,
        database="db_Invoice")
    cursor = db.cursor()
    del_sql = """
        DELETE FROM tb_invoice WHERE id NOT IN (
            SELECT id FROM (
                SELECT MIN(id) AS id
                FROM tb_invoice
                GROUP BY invoice_code
            ) AS temp_table
        );
    """
    cursor.execute(del_sql)
    db.commit()
    db.close()


    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_test.Ui_IncoiceDetectorUI()
    ui.setupUi(MainWindow)
    ui.actionDocumentation.triggered.connect(open_help_web)
    ui.pushButton_choose_file.clicked.connect(get_account_and_password)
    # Connect the choose botton
    ui.pushButton_choose_Folder.clicked.connect(browse_folder)
    #ui.pushButton_choose_file.clicked.connect(browse_file)
    ui.pushButton_Detect.clicked.connect(run_detector)
    ui.pushButton_search.clicked.connect(Search_button_clicked)

    ui.pushButton_add.clicked.connect(add_invoice)
    ui.pushButton_mod.clicked.connect(modify_invoice)
    ui.pushButton_del.clicked.connect(delete_invoice)



    MainWindow.show()
    sys.exit(app.exec())