# %%
# from posix import environ
from xmlrpc.client import boolean
import oracledb
import os 

def db_conn():

    # download oracle instant client for windows 32-bit 
    # https://www.oracle.com/ca-en/database/technologies/instant-client/microsoft-windows-32-downloads.html

    host="oracle.cs.torontomu.ca"
    uid= os.environ.get("ora_uid") 
    pwd= os.environ.get("ora_pwd") 

    oracledb.init_oracle_client(lib_dir="/Volumes/instantclient-basic-macos.arm64-23.3.0.23.09")

    return oracledb.connect(user=uid, password=pwd, host=host, port=1521, sid="orcl")
        
def db_ddl(script: str):
    error=""
    ok=True
    try:
        with db_conn() as connection:    
            with connection.cursor() as cursor:
                cursor.execute(script)
                cursor.execute("commit")
    except Exception as e:
        error=e
        ok=False
    return ok, error 

def db_sql(sql: str):

    columns = []
    data = []
    error = None
    try:
        with db_conn() as connection:    
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
    except Exception as e:
        error= e
        print("Error:", e)

    return columns, data , error

