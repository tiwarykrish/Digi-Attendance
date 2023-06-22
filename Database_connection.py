import mysql.connector as connector

class DBhelper:
    def __init__(self):
        self.con = connector.connect(host='localhost', port='3306', user='root', password='Ashu@2002', database='smartattendence_schema')
        query = 'create table if not exists user(username varchar(50),login_time datetime)'
        cur=self.con.cursor()
        cur.execute(query)
        print("created")
    def insert_user(self,username, login_time):
        query="insert into user(username, login_time) values('{}','{}')".format(username,login_time) 
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("data is inserted!!!!")

helper= DBhelper()
helper.insert_user("Ashish","03-18-2023 08:30:30")

