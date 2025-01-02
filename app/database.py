#1.导入 SQLAlchemy 部件
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from urllib.parse import quote_plus
import os, pymysql
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_STOCK')
}
# encoded_password = quote_plus(db_config['password'])
# connection_string = f"mysql+pymysql://{db_config['user']}:{encoded_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# #2.为 SQLAlchemy 定义数据库 URL地址
# #3.创建 SQLAlchemy 引擎
# engine = create_engine( connection_string )
# #4.创建一个SessionLocal 数据库会话
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
# #5.创建一个Base类
# Base = declarative_base()


conn = None
def get_conn():
    global conn
    if not conn:
        conn = pymysql.connect(host=db_config['host'], port=db_config['port'], user=db_config['user'], password=db_config['password'], 
                           database=db_config['database'], cursorclass=pymysql.cursors.DictCursor)
    return conn


def find_list(sql:str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    # cursor.close()
    # conn.close()
    return result