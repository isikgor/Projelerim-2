import sqlite3 as sql

class Database:

    def __init__(self,path):
        self.path = path
        self.connection = sql.connect(self.path)

    def get_tables(self):

        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM sqlite_sequence")
        records = self.cursor.fetchall()

        read = []

        for record in records:
            read.append(record[0])
        
        return read

    def get_all_records(self,table):
        read = {}

        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM "+table)
        records = self.cursor.fetchall()

        for record in records:
            read[record[0]] = {
                'name' : record[1],
                'address' : record[2],
                'date' : record[3]
            }
        self.cursor.close()
        return read


    def add_new_record(self,table,name,address,date):
        insert_query = f"""INSERT INTO {table}
                        (Ad_Soyad, Adres, Tarih) 
                        VALUES 
                        (?,?,?)"""
        
        self.cursor = self.connection.cursor()
        self.cursor.execute(insert_query,(name,address,date))

        self.connection.commit()

        self.cursor.close()


    def delete_record(self,table,id = int):
        delete_query = f"""DELETE from {table} where ID = %d""" %id
        
        self.cursor = self.connection.cursor()
        self.cursor.execute(delete_query)

        self.connection.commit()
        self.cursor.close()

    def update_record(self,table,id , name, address, date):

        update_query = f"""Update {table} SET 
                        Ad_Soyad = ?,
                        Adres = ?,
                        Tarih = ?
          WHERE ID = ?"""
        self.cursor = self.connection.cursor()
        self.cursor.execute(update_query,(name,address,date,id))

        self.connection.commit()
        self.cursor.close()

