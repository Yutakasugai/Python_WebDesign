from os import wait
import sqlite3

class WarehouseDB:
    def __init__(self, dbName):
        self.dbname = dbName
        self.conn = ''

    # Create a Database if it doesn't exit or connect to the spcified database
    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.dbname)
            return self.conn
        except Exception as e:
            print(str(e))

    # Create tables for our main program (Budget)
    # This function is only run once in the progam lifecycle
    def create_table(self):
        # Put autoincrement value back to all tables after Primary key

        sql_table1 = """ create table if not EXISTS agent_list(
                            ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            Name text NOT NULL
                            )"""

        sql_table2 = """ create table if not EXISTS trx(
                            ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            Time text NOT NULL,
                            Data text NOT NULL,
                            Device_Name text NOT NULL,
                            Note text NOT NULL,
                            Agent text NOT NULL, 
                            Result text
                            )"""
        
        sql_table3 = """create table if not EXISTS userLog(
                            ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            nameUser text NOT NULL,
                            password text NOT NULL
                            )"""
        
        sql_table4 = """create table if not EXISTS adminLog(
                            ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            nameAd text NOT NULL,
                            passwordAd text NOT NULL
                            )"""


        sql_table = [sql_table1, sql_table2, sql_table3, sql_table4]

        try:
            c = self.conn.cursor()
            for item in sql_table:
                c.execute(item)

        except Exception as e:
            print(str(e))

    # Show the values from tables.
    # Table_name can be "Food_Record, Necessity_Record, Enter_Record"
    def show_all(self, table_Name):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM {}".format(table_Name))
            items = c.fetchall()
            for item in items:
                print("\t{}".format(item))
            self.conn.commit()
        except Exception as e:
            print(str(e))

    def add_user(self, adminName, password):
        try:
            c = self.conn.cursor()

            c.execute("INSERT INTO adminLog (nameAd, passwordAd) VALUES (?, ?)", (adminName, password))
            self.conn.commit()

            # Check if the value is succesfully added to the table or not
            print("\n\tAdded a new item in the DB")

        except Exception as e:
            print(str(e))
    # Add new values in databese tables
    def add_item(self, item, price, table_name):
        try:
            c = self.conn.cursor()

            c.execute("INSERT INTO {}(item, price) VALUES (?,?)".format(
                table_name), (item, price))
            self.conn.commit()

            # Check if the value is succesfully added to the table or not
            print("\n\tAdded a new item in the DB")

        except Exception as e:
            print(str(e))

    # Delete values from database tables
    def delete_item(self, id, table_name):
        try:
            c = self.conn.cursor()
            c.execute("DELETE from {} WHERE ID = (?)".format(table_name), id)
            self.conn.commit()
        except Exception as e:
            print(str(e))

    # Check the tables if they have recored or not
    def check_table(self, table_name):
        try:
            c = self.conn.cursor()
            c.execute("SELECT COUNT(ID) FROM {}".format(table_name))
            # self.number_cell = (c.fetchone()[0])
            # item = 0
            item = (c.fetchone()[0])
            self.conn.commit()

            return item

        except Exception as e:
            print(str(e))

    # Calculate the total cost in the selected table
    def total_cost(self, table_name):
        try:
            c = self.conn.cursor()
            c.execute("SELECT price FROM {}".format(table_name))
            items = c.fetchall()
            total = 0
            for item in items:
                total = total + item[0]

            self.conn.commit()

            return total

        except Exception as e:
            print(str(e))

    # Close the databases
    def close_connection(self):
        self.conn.close()

def main():
    db = WarehouseDB('warehouse.db')
    db.create_connection()
    db.create_table()
    #db.add_user('admin', 'abc@123')
    db.close_connection()
main()