import pymysql

db = pymysql.connect(
host="localhost",
user="root",
password="root",
database="db_Invoice")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS tb_invoice")

sql = """CREATE TABLE tb_invoice (
id INT(8) NOT NULL AUTO_INCREMENT,
invoice_code varchar(50) NOT NULL,
date varchar(50) ,
buyer_code varchar(50),
buyer_name varchar(50),
seller_code varchar(50),
seller_name varchar(50),
invoice_amount_SMALL varchar(50),
note varchar(255),
PRIMARY KEY (id)
)"""
cursor.execute(sql)
db.close()
