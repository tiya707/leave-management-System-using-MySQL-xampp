# download xampp acoording to your OS 
# open phpmyadmin by localhost and create a database for eg: here leave_01 
# run this file on VScode and see the results on localhost

import mysql.connector
db= mysql.connector.connect(
    host="localhost", user="root", password="",database='leave_01')
command_handler=db.cursor(buffered=True)
mycursor = db.cursor()

def admin_session():
    print("")
    print("Admin Menu")
    while 1:
        print("")
        print("1. Register new employee")
        print("2. Delete Existing employee")
        print("3. Accept/Reject Leave")
        print("4. Logout" )
        choice=input(str("Option:"))
        if choice =="1":
            print("")
            print("Register New Employee")
            username= input(str("Employee Username :"))
            id= input(str("Employee id :"))
            password= input(str("Employee Password :"))
            email= input(str("Employee Email :"))
            phone= input(str("Employee Phone no :"))
            address= input(str("Employee Address :"))
            post= input(str("Employee Post :"))
            salary= input(str("Employee salary :"))
            query_vals= (id,username,password,email,phone,address,post,salary)
            command_handler.execute("INSERT into emp_data(Id,Username,Emp_Pass,Email_Id,Phone_no,Address,Post,Salary,Privilege) "
                                    "values(%s,%s,%s,%s,%s,%s,%s,%s,'Employee')",query_vals)
            db.commit()
            print(username + " has been resgistered as an employee")
        elif choice=="2":
            print("")
            print("Delete Existing Employee Account")
            username=input(str("Employee username :"))
            query_vals=(username,)
            command_handler.execute("DELETE from emp_data where Username = %s ",query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("user not found")
            else:
                print(username + " has been deleted ")
        elif choice=="3":
            acceptleave()
            
        elif choice == "4":
            break
        else:
            print("Invalid choice")

def updateleavestatus():
    update_list=[]
    id=input(str("Enter id :"))
    earnleave=input(str("Enter earnleaves :"))
    casualleave=input(str("Enter casualleave :"))
    sickleave=input(str("Enter sickleaves :"))
    otherleave=input(str("Enter otherleaves :"))
    update_list.append(earnleave)
    update_list.append(casualleave)
    update_list.append(sickleave)
    update_list.append(otherleave)
    update_list.append(id)
    update_tuple=tuple(update_list)
    sql=' UPDATE emp_data Set Earnleave=%s ,Casualleave=%s ,Sickleave=%s ,Otherleave=%s WHERE id=%s '
    command_handler.execute(sql,update_tuple)
    print("Data Updated")
    db.commit()  

def appr():
    update_list=[]
    id=input(str("Enter id :"))
    status=input(str("Enter status :" ))
    update_list.append(status)
    update_list.append(id)
    update_tuple=tuple(update_list)
    sql='UPDATE emp_reqleave Set Status_=%s where id=%s'
    command_handler.execute(sql,update_tuple)
    print("Done")
    db.commit()
    
def acceptleave():
    print("")
    id=input(str("Enter id :"))
    print("1. Earnleave")
    print("2. Casualleave")
    print("3. Sickleave ")
    print("4. Otherleave ")
    choiceofleave= input(str("Option :"))
    query_vals=(id,)
    command_handler.execute("SELECT Earnleave,Casualleave,Sickleave,Otherleave from emp_data WHERE id=%s ",query_vals)
    if choiceofleave=='1':
        appr()
    elif choiceofleave=='2':
        appr_disappr()
    elif choiceofleave=='3':
        appr()
    elif choiceofleave=='4':
        appr_disappr()
    else:
        print("Invalid choice")

def appr_disappr():
    print("")
    id=input(str("Enter id :"))
    query_vals=(id,)
    print("Casualleave,Otherleave")
    command_handler.execute('SELECT Casualleave,Otherleave from emp_data where Id=%s ',query_vals)
    records=command_handler.fetchall()
    for record in records:
        print(record)
    update_list=[]
    status=input(str("enter status :"))
    update_list.append(status)
    update_list.append(id)
    update_tuple=tuple(update_list)
    sql='UPDATE emp_reqleave Set Status_=%s where id=%s'
    command_handler.execute(sql,update_tuple)
    print("Done")
    db.commit()
        
def auth_admin():
    print("")
    print("Admin Login")
    print("")
    username=input(str("Username :"))
    password=input(str("Password :"))
    if username=="admin":
        if password=="password":
            admin_session()
        else:
            print("Incorrect Pass")
    else:
        print("Login details not recognised")
        
def applyleave(username):
    print("")
    print("Leave Apply")
    print("")
    
    print("Enter the following details :")
    print("Select type of leave")
    print("Type of leave :")
    print("1. Earnleave")
    print("2. Casualleave")
    print("3. Sickleave")
    print("4. Otherleave")
    choiceofleave= input(str("Option :"))
    leavetype=choiceofleave
    id=input(str("Empolyee id :"))
    username=input(str("Employee username :"))
    startdate=input(str("Leave startdate :"))
    enddate=input(str("Leave enddate :"))
    reqdate=input(str("Request date :"))
    post=input(str("Employee Post :"))
    query_vals=(id,username,leavetype,reqdate,startdate,enddate,post)
    
    command_handler.execute("INSERT INTO emp_reqleave(Id,Username,LeaveType,RequestDate,StartDate,EndDate,Post,Status_) VALUES (%s,%s,%s,%s,%s,%s,%s,'Pending') ",query_vals)
    print("Leave Applied")
    db.commit()
   

def employee_session(username):
    while 1:
        print("")
        print("Employee Menu")
        print("")
        print("1. Leave status")
        print("2. Update Leave status")
        print("3. Request a leave")
        print("4. Display Information")
        print("5. Logout")
        
        choice=input(str("Option :"))
        if choice =='1':
            print("")
            print("Leave status")
            username=(str(username),)
            print("Earnleave,Casualleave,Sickleave,Otherleave")
            command_handler.execute("SELECT Earnleave,Casualleave,Sickleave,Otherleave from emp_data where Username= %s",username)
            records=command_handler.fetchall()
            for record in records:
                print(record)
            command_handler.execute("SELECT Status_ from emp_reqleave where Username=%s",username)
            records1=command_handler.fetchall()
            for record in records1:
                print(record)
            
        elif choice=="2":
            updateleavestatus()
        elif choice=="3":
            applyleave(username)
            
        elif choice=="4":
            id=input(str("Enter Id :"))
            query_vals=(id,)
            command_handler.execute("SELECT * from emp_data where Id=%s",query_vals)
            records=command_handler.fetchall()
            for record in records:
                print(record)
        elif choice=='5':
            break
        else:
            print("Invalid choice")
        
def auth_emp():
    print("")
    print("Employee Login")
    print("")
    username=input(str("Username :"))
    password=input(str("Password :"))
    query_vals=(username,password,"Employee")
    command_handler.execute("SELECT * from emp_data where Username= %s And Emp_Pass= %s And privilege = %s ",query_vals)
    if command_handler.rowcount <= 0:
        print("Login not recognised")
    else:
        print("Welcome Employee")
        employee_session(username)
                
def main():
    while 1:
        txt="Welcome To The Leave Management System"
        x=txt.center(450)
        print(x)
        print("1. Login As Admin")
        print("2. Login As An Employee")
        choice=input(str("Option:"))
        
        if choice=="1":
            auth_admin()
        elif choice=="2":
            auth_emp()
        else:
            print("InValid Option Selected")
main()
