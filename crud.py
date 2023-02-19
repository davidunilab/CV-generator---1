import sqlite3

class CRUD:
    def __init__(self):
        self.con = sqlite3.connect("C:\Users\HP\Desktop\UNILAB-PYTHON\Final Project\CV generator - 1\cv_builder.db")
        self.cur = self.con.cursor()
        
    
    def create_table(self, table_name, array):
        query = f""" CREATE TABLE IF NOT EXISTS {table_name} """
        query + f"("
        for i in array:
            query += f"{i},"
        query += ");"
        query -= ','
        self.cur.execute()
        
    
    def insert(self, table):
        ins = self.cur.execute(f"insert into {table} values")
        return ins.fetchall()
    
    def select(self, table_name,  where=[] ):
        res = self.cur.execute(f"select * from {table_name} where{where}")
        return res.fetchall()
    
    
    def update(self, table_name, where):
        update = self.cur.execute(f"update * {table_name} set where {where}")
        return update.fetchall()
        
    def delete(self, table_name):
        delete = self.cur.execute(f'delete from {table_name} where t1 = ?')
        return delete.fetchall()
    
    
    
db = CRUD()
db.create_table("user", ["id",'name', "surname", "email"])
