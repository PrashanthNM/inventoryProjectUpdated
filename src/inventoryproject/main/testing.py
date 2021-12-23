import mysql.connector

#the below funtion computes the reorder table into a dictionary my_dictis
def compute_reorder_table():
    cur=db.cursor()
    cur.execute("SELECT *  FROM dataset")
    table = cur.fetchall()
    lead_y=0
    count=1
    batch=0
    a=[]
    for lists in table:
        d=lists[0]
        x=lists[3]
        y=lists[4]
        if x!=0 :
            stock=x
            lead_x=d 
        elif y!=0 :
            batch+=y
            lead_y=lead_y+(d-lead_x)
            if(batch==stock):
                a.append([batch,lead_y/count])
                batch=0
                count=0
                lead_y=0
            count+=1
        a.sort()
    dictis ={}
    for i in a:
        if i[0] in dictis.keys():
            dictis[i[0]].append(i[1])

        else:
            ll=[]
            ll.append(i[1])
            dictis[i[0]] = ll
    my_dictis={}
    for vals in dictis:
        sums=0
        for i in dictis[vals]:
            sums = sums + i
        my_dictis[vals] = [len(dictis[vals])]
        my_dictis[vals].append(sums/len(dictis[vals]))
        my_dictis[vals].append(my_dictis[vals][0]/len(a))
    return my_dictis

#the below saved table is the dataset value  
saved_table = [[50, 3, 0, 0],
[47, 6, 0, 0],
 [41, 4, 0, 0],
 [37, 6, 0, 0],
 [31, 8, 50, 0],
 [23, 4, 0, 0],
 [19, 12, 0, 0],
 [7, 9, 0, 50],
 [48, 4, 0, 0],
 [44, 7, 0, 0],
 [37, 10, 0, 0],
 [27, 8, 0, 0],
 [19, 7, 50, 0],
 [12, 9, 0, 50],
 [53, 7, 0, 0],
 [46, 2, 0, 0],
 [44, 12, 60, 0],
 [32, 3, 0, 0],
 [29, 10, 0, 0],
 [19, 7, 0, 60]]

#connction to the database
db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="2580",
    database ='testdatabase'
    
)
#TABLE FORMAT
#[DAY,STOCK,SALES,REORDER_QUANTITY,ORDER_RECEIVED]
cur=db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS dataset(id INT AUTO_INCREMENT PRIMARY KEY,stock int,sales int,reorder_quantity int ,order_received int)")

#this funtion creates the table dataset using the saved_table values
def create_dataset_table():
    cur=db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS dataset(id INT AUTO_INCREMENT PRIMARY KEY,stock int,sales int,reorder_quantity int ,order_received int)")
    query="INSERT INTO dataset(stock,sales,reorder_quantity,order_received) VALUES (%s,%s,%s,%s)"
    sales_quantity = 0
    order_quantity = 0
    for values in saved_table:
        cur.execute(query,(values[0],values[1],values[2],values[3] ))
        sales_quantity = sales_quantity + values[1]
        order_quantity = order_quantity + values[2]
    db.commit()
    cur = db.cursor()
    query = "INSERT INTO quantity(cost,sales_quantity,order_quantity) VALUES (%s,%s,%s)"
    value=(10,sales_quantity,order_quantity)
    cur.execute(query,value)
    db.commit()





#using the dataset table this functio creates frequncy table
def create_frequency_table():
    data={}
    cur=db.cursor()
    #selecting sales column from the datset
    cur.execute("SELECT sales  FROM dataset")
    sales_data = cur.fetchall()
    for val in sales_data:
        if val[0] in data.keys():
            data[val[0]] = data[val[0]] + 1
        else:
            data[val[0]]  = 1
    cur=db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sales_frequency(id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,sales_quantity int, sales_frequency int ,pq double )")

    for key in data:
        query = "INSERT INTO sales_frequency(sales_quantity,sales_frequency,pq) VALUES (%s,%s,%s)"
        var = data[key]/len(sales_data)
        values = (key,data[key],var)
        cur.execute(query,values)
    db.commit()

#using the dataset table this function creates reorder_table table
def create_reorder_table():
    cur=db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS reorder_table(id INT AUTO_INCREMENT PRIMARY KEY,reorder_quantity int,frequency int,lead_time int ,plql float)")
    my_dict = compute_reorder_table()
    query = "INSERT INTO reorder_table(reorder_quantity,frequency,lead_time,plql) VALUES (%s,%s,%s,%s)"
    for val in my_dict:
        values = (val,my_dict[val][0],my_dict[val][1],my_dict[val][2])
        cur.execute(query,values)
    db.commit()

#using the dataset table this function creates table called demand_ql
def create_demand_ql():
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS demand_ql(id INT AUTO_INCREMENT PRIMARY KEY,reorder_quantity int,lead_time float,plql float,ql float )")
    cur.execute("SELECT *  FROM reorder_table")
    sales_data = cur.fetchall()
    query = "INSERT INTO demand_ql(reorder_quantity,lead_time,plql,ql) VALUES (%s,%s,%s,%s)"
    # var = vals/my_dictis[vals][1])*find_l()
    for i in range(len(sales_data)):
        var = (sales_data[i][1]/sales_data[i][3])*find_l(sales_data)
        values = (sales_data[i][1],sales_data[i][3],sales_data[i][4],var)
        cur.execute(query,values)
    db.commit()

#this table creates a table called lead time with ptr and lead_time columns
def create_lead_time():
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS lead_time(id INT AUTO_INCREMENT PRIMARY KEY,quantity int,lead_time int,ptr int,is_lead_time boolean )")
    db.commit()



#to find m uisng algorithm
def find_m():
    cur=db.cursor()
    cur.execute("SELECT *  FROM sales_frequency")
    sales_data = cur.fetchall()
    m=0
    for val in sales_data:
        m = m + val[1]*val[3]
    return m

#to find m uisng algorithm
def find_l(table):
    #L = SUMMATION(Q0*lo)/summation(q0)
    num=0
    den=0
    for row in table:
        num = num + row[1]*row[3]
        den = den + row[1]
    return (num/den)

#to find m uisng algorithm     
def find_ml():
    ml=0
    cur = db.cursor()
    cur.execute("SELECT *  FROM demand_ql")
    table = cur.fetchall()
    for rows in table:
        ml = ml + rows[3]*rows[4]
    return ml

#to create qunatity table which keeps the track of sales_quantity and order quantity
def create_quantity():
    cur.execute("CREATE TABLE IF NOT EXISTS quantity(id INT AUTO_INCREMENT PRIMARY KEY,cost float,sales_quantity int,order_quantity int)")


# print(find_m())
# print(find_l())
# print(find_ml())

# find_ql()



def print_my():
    print(f" m = {find_m()}")
    print(f" ml = {find_ml()} ")
    print("\n")

create_quantity()
create_dataset_table()
create_frequency_table()
create_reorder_table()
create_demand_ql()
create_lead_time()
print_my()



