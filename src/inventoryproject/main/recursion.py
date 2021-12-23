import math
import mysql.connector
# from main.testing2 import *
from main.testing2 import find_m,find_ml



def S_fun(R):
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="testdatabase") 

    cursor = db.cursor()
    cursor.execute("SELECT ql,plql FROM demand_ql ORDER BY plql")
    S=cursor.fetchall()
    print(S)
    val=0
    for x,y in S:
        val += y
        if R<val or R==val :
            return x     

def sum_pLqL(s):
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="testdatabase") 

    cursor = db.cursor()
    cursor.execute("SELECT ql,plql FROM demand_ql WHERE qL>'%s'",[s])
    dict = cursor. fetchall()
    exp=0
    for qL,pL_qL in dict:
        exp += (qL-s)*pL_qL
    return exp

def recursion(h,Q,ML,M,pi,k,prev_s):
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="testdatabase") 
    prev_s = round(prev_s)
    R = 1-(h*Q/(0.5*h*ML+M*pi))
    print(f"R is {R}")
    s = S_fun(R)
    print(s)
#     print(f" s = {s} prev_s = {prev_s}")
    if round(s)==prev_s :
        return (s,round(Q))

    pL_qL = float(sum_pLqL(s))
    Q = math.sqrt( ((2*k*M)/h) + ((ML+((2*M*pi)/h))*pL_qL)  )
    return recursion(h,Q,ML,M,pi,k,s)

def calculate_s_Q():
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="testdatabase") 
    c = 10
    k = 312.5
    h = 2
    pi= 2.5
    ML = find_ml()
    M = find_m()
    
    Q = round(math.sqrt((2*k*M)/h))
  
    s,Q = recursion(h,Q,ML,M,pi,k,0)
    s = round(s)
    return (s,Q)
    
#     cursor.execute("SELECT NUM_STOCK FROM PEN ORDER BY NUM_STOCK DESC")
#     current_stock=cursor.fetchone()[0]
    
#     if(Q>current_stock):
#         print("place order")
print(calculate_s_Q())