import mysql.connector

mydb = mysql.connector.connect(
	host='localhost',
	user="ades",
	passwd="admin123"
)

my_cursor= mydb.cursor()
#my_cursor.execute("CREATE DATABASE flaskblog")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
	print(db)