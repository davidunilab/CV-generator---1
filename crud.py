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
        self.cur.execute()
        
    
    def create(self, table_name, *args):
       pass

    
    def select(self, table_name,  where=[] ):
        res = self.cur.execute(f"select * from {table_name} where{where}")
        return res.fetchall()
    
    
    def update(self):
        pass
    
    def delete(self):
        pass
    
    
    
db = CRUD()
db.create_table("user", ["id",'name', "surname", "email"])
