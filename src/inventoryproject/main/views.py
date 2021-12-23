#A view function is a Python function that takes a Web request
#  and returns a Web response. This response can be the HTML contents of a Web page,
#  or a redirect, or a 404 error, or an XML document, or an image, anything that a web browser can display

from re import fullmatch
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from main.testing2 import *
from main.check import insert


#by default this function returns the home page
def homePage(request,*args,**kwargs):
    return render(request,'index.html')

#this functions updates the dashboard dynamically from te quantity database
def admins(request,*args,**kwargs):
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="testdatabase") 
    cur = db.cursor()
    cur.execute("SELECT * FROM quantity")
    s = cur.fetchall()
    #this dictionary is passed to the admin.html page to dispaly the values in the dashboard 
    my_dict={
        'sales_quantity':s[0][2],
        'order_quantity':s[0][3],
        'order_cost':s[0][3]*10,
        'sales_cost':s[0][2]*14
    }
    return render(request,'admin.html',my_dict)

#funtion for regustering the users
def register(request,*args,**kwargs):
    if(request.method == 'POST'):
        name=request.POST['name'] #gets value from the frontend 
        password=request.POST['password']
        if User.objects.filter(username=name).exists(): #checks if the user requests
             messages.info(request,'Username Taken')
             return redirect('register') #redirects the register page again
        else:
            user = User.objects.create_user(username=name, password=password)
            user.save() #its saves the users id and password in the databasse
        return redirect('login')
    return render(request,'register.html')

def login(request,*args,**kwargs):
    if request.method=="POST":
        global name
        name=request.POST['name']
        password=request.POST['password']
        user=auth.authenticate(username=name,password=password)

        if user is not None: #if user id and password is same
            auth.login(request,user)

            return redirect('admins')
        else:
            messages.info(request,'invalid credentials')
            return render(request,"login.html")   

    return render(request,'login.html')



def logout(request):
    auth.logout(request)
    return redirect('/')


def sell(request,*args,**kwargs):
    return render(request,'sell.html')

def supplier(request,*args,**kwargs):
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="testdatabase") 
    curdict = db.cursor(dictionary=True)
    curdict.execute("SELECT * FROM supplier")
    val=curdict.fetchall()
    context={ "val" : val }
    return render(request,'supplier.html',context)

    
def addsup(request,*args,**kwargs):
        if(request.method == 'POST'):
            FullName=request.POST.get('FullName')
            ItemName = request.POST.get('ItemName')
            invoice = request.POST.get('invoice')
            print(FullName,ItemName,invoice)
            db = mysql.connector.connect(host="localhost",user="root",password="2580",database="testdatabase") 
            cursor = db.cursor()
            values= (FullName,ItemName,invoice)
            cursor.execute("INSERT INTO supplier(name,item_name,invoice) VALUES(%s,%s,%s)",values)
            db.commit()
            curdict = db.cursor(dictionary=True)
            curdict.execute("SELECT * FROM supplier")
            val=curdict.fetchall()
            context={ "val" : val }
            return redirect('supplier')
            # return render(request,'supplier.html',context)

        return render(request,'addsup.html')


#this function gets the sales_quantity entered in the frontend(purchase.html) 
#and updates the tables in the database
def purchase(request,*args,**kwargs): 
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="testdatabase") 
    cur = db.cursor()
    cur.execute("SELECT * FROM dataset")
    s = cur.fetchall()
    present_stock_count = s[len(s)-1][1] - s[len(s)-1][2] + s[len(s)-1][4]
    my_dict={
        'present_stock_count':present_stock_count
    }
    #the below if statememts checks if all the feilds are filled
    #if not it sends a message telling to enter all the feilds in the frontend

    if(request.method == 'POST'):
        qty=request.POST.get('qty')
        invoice = request.POST.get('invoice')
        sname = request.POST.get('sname')
        print(qty,sname,invoice)
        if(invoice == ''):
            messages.info(request,'invoice cannot be empty')
            return render(request,"purchase.html",my_dict) 
        elif(qty == ''):
            messages.info(request,'quantity cannot be empty')
            return render(request,"purchase.html",my_dict) 
        elif(sname == ''):
            messages.info(request,'Ssupplier name cannot be empty')
            return render(request,"purchase.html",my_dict) 
        elif(qty!='0' and qty!=''):
            insert(int(qty))  
        return redirect('admins')
    
    curdict = db.cursor(dictionary=True)
    curdict.execute("SELECT * FROM supplier")
    val=curdict.fetchall()

    context={ "val" : val,
    'present_stock_count': present_stock_count,
    }
    return render(request,'purchase.html',context)
