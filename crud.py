import sqlite3

class CRUD:
    def __init__(self):
        self.con = sqlite3.connect("cv_builder.db")
        self.cur = self.con.cursor()
        
    
    def create_table(self, table_name, array):
        query = f""" CREATE TABLE IF NOT EXISTS {table_name} """
        query + f"("
        for i in array:
            query += f"{i},"
        query = query[:-1]
        query += ");" 
        print(query)
        self.cur.execute(query)
        
    
    def insert(self, table_name, **args):
        stmt = ""
        stmt += f"INSERT INRO{table_name} VALUES ("
        
        for item in args:
            stmt += f""" '{item}' , """
            
        stmt = stmt[:-1]
        stmt += ");"
        print(stmt)
        
        self.cur.execute(stmt)
        self.con.commit()
        
    
    def select(self, table_name,  where=[]):
        if not where:
            stmt = f"select * from {table_name}"
        else:
           stmt = f"select * from {table_name} where {where}"
       
        print(stmt)
        
        res = self.cur.execute(stmt)
        return res.fetchall()
        
        
    def update(self, table_name, datum, condition):
        stmt = f"UPDATE {table_name} SET"
        for k, v in datum.items():
            stmt += f"{k} = '{v}' , "
        stmt = stmt[:-1]
        
        stmt += "where"
        for k, v in condition.items():
            stmt += f"{k} = '{v}' , "
        stmt = stmt[:-1]
        stmt += ";"
        
        print(stmt)
        self.cur.execute(stmt)
        self.con.commit()
            
        
    def delete(self, table_name, column, value):
       stmt = ""
       stmt += f"DELETE FROM {table_name} where {column} = '{value}';"
       self.cur.execute(stmt)
       self.con.commit()
       
       
    
db = CRUD()
db.create_table("user", ["id",'name', "surname", "email"])






db.insert("user", 1, "John", "Doe", "johnDoe@gmail.com")


data = {"name": "Jouaqin", "email": "Jouaqin@gmail.com"}
where = {"id": '1'}
db.update("user", data, where)

db.delete("user", "id", "1")

print(db.select("user", "id, = '1'"))
