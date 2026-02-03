import uuid
from contextlib import contextmanager
from logging import exception
import datetime

import psycopg2
import sqlalchemy

class ConnectionFieldError:
    pass
class QueryTimeoutError:
    pass
class MaxRetriesExceededError:
    pass


class Connect_db:

        choice= {1:"active" ,0:"idle"}
        def __init__(self):
            self.connection_id = uuid.uuid4()
            self.status = "idle"
            self.created_at = datetime.datetime.now()


        def is_alive(self):
            if self.db.closed == 0:
                self.is_alive(True)
                print("Connection is open (according to the client).")
            else:
                self.is_alive(False)
                print("Connection is closed or in a broken state.")

        def connectt(self):
            try:
                with psycopg2.connect("postgresql://postgres:ugWrWQWzzFoTeCGdbzNKQaLTWPEGRswz@yamabiko.proxy.rlwy.net:22331/railway") as conn:
                    self.db = conn
                    self.status = "active"

            except psycopg2.OperationalError as e:
                print("unable to connect database:",{e})
            else:
                print("database connected",self.connection_id)

        def disconnect(self):
          try:
           self.conn.close()
           self.status = "idle"
          except Exception as e :
              print("field closing",e)
          else:
              print("closed connection")


        def execute_query(self,query):
           try:
            with self.db.cursor() as cur:
                cur.execute(query)
                self.db.commit()
           except Exception as e:
               print("field to execute query",e)
           else:
               print("executed")

class ConnectionPool:
    def __init__(self):
        self.connection_pool =[]
        self.in_use =[]
        self.max_connection = 5

    def get_connection(self):
      try:
        if self.connection_pool:
            conn= self.connection_pool.pop()
            self.in_use= conn
            # self.connection_pool.remove(conn)
            print("connection retrieved with id:",conn.connection_id)
            return conn
        else:
            if len(self.connection_pool ) +len(self.in_use) <=5:
                conn = Connect_db()
                conn.connectt()
                # self.connection_pool.append(db)
                self.in_use.append(conn)
                print("connection retrieved with id " ,conn.connection_id)
                return conn
            else:
                raise "max limit reached"
      except Exception as e:
          print("field to get connection",e)



    def release_connection(self,conn):
        if conn:
                self.connection_pool.append(conn)
                self.in_use.remove(conn)
        else:
            print("connection not provided")



    def close_all(self):
        try:
            for db in self.in_use,self.connection_pool:
                print(db)
                db.disconnect()
        except Exception as e:
            print("field to close all connection:",e)
        else:
            print("connections closed succesfully")


    def get_stats(self):

        pass


# db1 = Connect_db()
# db1.connectt()
# db1.execute_query("""CREATE TABLE employees (
#                 emp_id SERIAL PRIMARY KEY,
#                 first_name VARCHAR(50) NOT NULL,
#                 last_name VARCHAR(50) NOT NULL,
#                 salary DECIMAL(10, 2)
#             );"""
# )
# db1.execute_query("""insert into employees (
#                 emp_id,first_name, last_name,salary) values (23,'pravesh','yadav',10000)
#             ;"""
# )

obj =ConnectionPool()
obj.get_connection()
obj.get_connection()
obj.get_connection()
obj.get_connection()
obj.get_connection()
obj.close_all()

