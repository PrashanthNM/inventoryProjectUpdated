import mysql.connector

db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="2580",
    database ='testdatabase'
    
)
# cursor = db.cursor()

cur = db.cursor()

cur.execute("DROP TABLE dataset")

cur.execute("DROP TABLE sales_frequency")
cur.execute("DROP TABLE reorder_table")
cur.execute("DROP TABLE demand_ql")
cur.execute("DROP TABLE lead_time")
cur.execute("DROP TABLE quantity")


