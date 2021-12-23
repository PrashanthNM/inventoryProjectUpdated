import math
from main.testing2 import insert_lead_time
from main.testing2 import insert_in_dataset
from main.recursion import calculate_s_Q
import mysql.connector
import random
from main.mail import send_mail

#this function insetrs the sales data along with order_aquantity(if required)
#according to the algorithm used in the function
def insert(var):
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="testdatabase")
    cur = db.cursor()
    a=calculate_s_Q() #calculate_s_Q untion returns a tuple which contains (s,Q)
    s=a[0]
    Q=a[1]
    cur.execute("SELECT * FROM quantity")
    quantity_data = cur.fetchall()
    print(quantity_data)
    #thise two variables below keep track of the present sales quantity and ordered quantitu
    sales_quantity = quantity_data[0][2] 
    order_quantity = quantity_data[0][3]


    sales_quantity = sales_quantity + var
    

    cur.execute("SELECT * FROM dataset")
    dicti = cur. fetchall()
    present_stock_qty = dicti[len(dicti)-1][1] -  dicti[len(dicti)-1][2] +  dicti[len(dicti)-1][4]
    temp = dicti[len(dicti)-1][3]
    cur.execute("SELECT * FROM lead_time")
    lead_time_data = cur.fetchall()

    #the below if-else statements checks if the leadtime is zero and 
    # updates the database accordingly
    if(len(lead_time_data) != 0):
        is_lead_time = lead_time_data[len(lead_time_data)-1][4]
        
    else:
        is_lead_time = 0
    if(is_lead_time == 1):
        #decrement ptr and if ptr = 0 insert the qunatity value in ordre received place 
        id =  lead_time_data[len(lead_time_data)-1][0]
        ptr = lead_time_data[len(lead_time_data)-1][3]
        Q = lead_time_data[len(lead_time_data)-1][1]
        ptr = ptr - 1

        #once the leadtime becomes zero ptr becomes zero and the order is received
        #this if else statement takes care of it
        
        if(ptr != 0):
            query = "UPDATE lead_time SET ptr = %s WHERE id = %s"
            values = (ptr,id)
            insert_in_dataset(var,0,0)
            cur.execute(query,values)
            db.commit()
        else:
            query ='UPDATE lead_time SET ptr = %s, is_lead_time = %s WHERE id = %s'
            values = (ptr,False,id)
            cur.execute(query,values)
            db.commit()
            send_mail(Q,"received")
            insert_in_dataset(var,0,Q)
            order_quantity = order_quantity + Q


    #if the value of s is greater the the present stock quantity we place the order
    #else we dont
    elif(s>=present_stock_qty):
        send_mail(Q,"ordered")
        insert_in_dataset(var,Q,0)
        time = random.randint(1,4)
        insert_lead_time(Q,time)
        print(Q,time)

    else:
        insert_in_dataset(var,0,0)

    #we update the sales_quantity and order quantity in the table quantity
    query1 = "UPDATE quantity SET sales_quantity = %s,order_quantity = %s WHERE  id =%s"
    values = (sales_quantity,order_quantity,1)
    cur.execute(query1,values)
    db.commit()
