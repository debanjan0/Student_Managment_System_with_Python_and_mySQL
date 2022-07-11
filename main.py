import mysql.connector
from datetime import date
import os

try:
    from tabulate import tabulate
except ModuleNotFoundError:
    os.system("pip install tabulate")
    from tabulate import tabulate

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)
A
mycursor = mydb.cursor()
today = date.today()
d1 = today.strftime("%Y/%m/%d")


def database_creation():
    sql = "CREATE DATABASE IF NOT EXISTS student" # creats database if not exist
    mycursor.execute(sql)
    mycursor.execute("use student")
    sql_stu_data='''
                CREATE TABLE IF NOT EXISTS student_data
                (sid integer primary key,
                name varchar(20),
                dob date,
                phone integer,
                city char(15),
                class integer);
                '''
    sql_stu_mark='''
                CREATE TABLE IF NOT EXISTS student_marks
                (tid integer primary key,
                sid integer,
                pyear integer,
                class integer,
                sroll integer,
                tmarks integer
                FOREIGN KEY (sid) REFERENCES student_data (sid)));
                '''
    sql_stu_fee='''
                CREATE TABLE IF NOT EXISTS fees(
                txid integer primary key AUTO_INCREMENT,
                sid integer NOT NULL,
                amount integer ,
                pay_date date,
                MoP char(50),
                FOREIGN KEY (sid) REFERENCES student_data (sid));
                '''
    mycursor.execute(sql_stu_data) # creats student data table if not exist
    mycursor.execute(sql_stu_mark) # creats student marks table if not exist
    mycursor.execute(sql_stu_fee)  # creats fees table if not exist


def student_data():
    mycursor.execute("select * from student_data ORDER BY sid")
    result = mycursor.fetchall()
    return result


def student_marks():
    mycursor.execute("SELECT * FROM student_marks ORDER BY tid")
    result = mycursor.fetchall()
    return result


def student_fees():
    mycursor.execute("SELECT * FROM fees ORDER BY txid")
    result = mycursor.fetchall()
    return result


def add_student():
    iid = int(input("Enter the id :- "))
    name = input("Enter the name :- ")
    dob = input("Enter the dob (year/month/day) :- ")
    no = int(input("Enter the number :- "))
    city = input("Enter the city :- ")
    clas = int(input("Enter the class :- "))
    sql = "INSERT INTO student_data (sid,name,dob,phone,city,class) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (iid, name, dob, no, city, clas)
    mycursor.execute(sql, val)
    mydb.commit()


def add_student_marks():
    tid = int(input("Enter the id :- "))
    sid = int(input("Enter the student id :- "))
    pyear = input("Enter the passing year :- ")
    clas = int(input("Enter the class :- "))
    sroll = int(input("Enter the roll number :- "))
    tmarks = int(input("Enter the total marks :- "))
    sql = "INSERT INTO student_marks (tid,sid,pyear,class,sroll,tmarks) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (tid, sid, pyear, clas, sroll, tmarks)
    mycursor.execute(sql, val)
    mydb.commit()


def add_fees():
    sid = input("Enter the student id:- ")
    amount = input("Enter the amount:- ")
    MoP = input("Enter the mode of payment (online/offline/check) :-")
    sql = "INSERT INTO fees (sid,amount,pay_date,MoP) VALUES (%s, %s, %s, %s)"
    val = (sid, amount, d1, MoP)
    mycursor.execute(sql, val)
    mydb.commit()


database_creation()


while True:
    data = []
    print("")
    print("1.To show the student details")
    print("2.To add student ")
    print("3.To show student marks")
    print("4.To give student marks")
    print("5.To show the fees record")
    print("6.To take fees")
    print("7.To exit")
    print("")
    n=int(input("Enter the number :- "))

    if n == 1:
        myresult = student_data()
        for x in myresult:
            data.append(x)
        print (tabulate(data, headers=["ID", "Name", "Date of birth", "Number", "City", "Class"]))
    elif n == 2:
        add_student()
    elif n == 3:
        myresult = student_marks()
        for x in myresult:
            data.append(x)
        print (tabulate(data, headers=["Marks ID", "Student ID", "Passing Year", "Class", "Roll No.", "Total marks"]))
    elif n == 4:
        add_student_marks()
    elif n == 5:
        myresult = student_fees()
        for x in myresult:
            data.append(x)
        print (tabulate(data, headers=["Payment ID", "Student ID", "Amount", "Payment date", "Mode of payment"]))
    elif n == 6:
        add_fees()
    elif n == 7:
        break
    else:
        print("enter a valid no")

