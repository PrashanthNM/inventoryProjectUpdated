import mysql.connector

#should update the tables
# from testing import compute_reorder_table
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
        # my_dictis[vals].append( (vals/my_dictis[vals][1])*find_l() )
    return my_dictis

#connction to the database
db=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="2580",
        database ='testdatabase',
        auth_plugin='mysql_native_password',  
    )

#to find m
def find_m():
    cur=db.cursor()
    cur.execute("SELECT *  FROM sales_frequency")
    sales_data = cur.fetchall()
    m=0
    for val in sales_data:
        if(val[1]==None or val[2]==None):
            continue
        m = m + val[1]*val[3]
    return m

#to find ml
def find_ml():
    ml=0
    cur = db.cursor()
    cur.execute("SELECT *  FROM demand_ql")
    table = cur.fetchall()
    for rows in table:
        ml = ml + rows[3]*rows[4]
    return ml
    
#to find l
def find_l(table):
    #L = SUMMATION(Q0*lo)/summation(q0)
    num=0
    den=0
    for row in table:
        num = num + row[1]*row[3]
        den = den + row[1]
    return (num/den)

        


#this funtion creates the table dataset using the saved_table values
def insert_in_dataset(val1,val2,val3):
    cur = db.cursor()
    query = "INSERT INTO dataset(stock,sales,reorder_quantity,order_received) VALUES (%s,%s,%s,%s)"
    cur.execute("SELECT *  FROM dataset")
    sales_data = cur.fetchall()
    stock_present = sales_data[len(sales_data)-1][1] + sales_data[len(sales_data)-1][4] - sales_data[len(sales_data)-1][2]
    cur.execute(query,(stock_present,val1,val2,val3))
    cur.execute("SELECT *  FROM dataset")
    sales_data = cur.fetchall()
    db.commit()
    update_frequency_table()
    update_reorder_table()
    update_demand_ql()
    
    

#using the dataset table this functio creates frequncy table
def update_frequency_table():
    data = {}
    cur=db.cursor()

    cur.execute("SELECT sales  FROM dataset")
    sales_data = cur.fetchall()
    for val in sales_data:
        if val[0] in data.keys():
            data[val[0]] = data[val[0]] + 1
        else:
            data[val[0]]  = 1
    cur=db.cursor()
    cur.execute("DROP TABLE sales_frequency")
    cur.execute("CREATE TABLE IF NOT EXISTS sales_frequency(id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,sales_quantity int, sales_frequency int ,pq double )")
    for key in data:
        query = "INSERT INTO sales_frequency(sales_quantity,sales_frequency,pq) VALUES (%s,%s,%s)"
       
        var    = data[key]/len(sales_data)
        values = (key,data[key],var)
        cur.execute(query,values)
    db.commit()

#using the dataset table this function creates reorder_table table
def update_reorder_table():
    cur=db.cursor()
    cur.execute("DROP TABLE reorder_table")
    cur.execute("CREATE TABLE IF NOT EXISTS reorder_table(id INT AUTO_INCREMENT PRIMARY KEY,reorder_quantity int,frequency int,lead_time int ,plql float)")
    my_dict = compute_reorder_table()
    query = "INSERT INTO reorder_table(reorder_quantity,frequency,lead_time,plql) VALUES (%s,%s,%s,%s)"
    for val in my_dict:
        values = (val,my_dict[val][0],my_dict[val][1],my_dict[val][2])
        cur.execute(query,values)
    db.commit()
def insert_lead_time(Q,time):
    cur = db.cursor()
    query = "INSERT INTO lead_time(quantity,lead_time,ptr,is_lead_time) VALUES (%s,%s,%s,%s)"
    values = (Q,time,time,1)
    cur.execute(query,values)
    db.commit()

#using the dataset table this function creates table called demand_ql
def update_demand_ql():
    cur = db.cursor()
    cur.execute("DROP TABLE demand_ql")
    cur.execute("CREATE TABLE IF NOT EXISTS demand_ql(id INT AUTO_INCREMENT PRIMARY KEY,reorder_quantity int,lead_time float,plql float,ql float )")
    cur.execute("SELECT *  FROM reorder_table")
    sales_data = cur.fetchall()
    query = "INSERT INTO demand_ql(reorder_quantity,lead_time,plql,ql) VALUES (%s,%s,%s,%s)"
    # var = vals/my_dictis[vals][1])*find_l()

    for i in range(len(sales_data)):
        var    = (sales_data[i][1]/sales_data[i][3])*find_l(sales_data)
        values = (sales_data[i][1],sales_data[i][3],sales_data[i][4],var)
        cur.execute(query,values)
    db.commit()


def print_m_ml():
    print(f" m = {find_m()}")
    print(f" ml = {find_ml()} ")
    print("\n")



print_m_ml()



