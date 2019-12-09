# 导入python内置的SQLite驱动:
import sqlite3
import os.path
import logging

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "word.db")


def create_table():
    """创建表"""

    # 连接到SQLite数据库
    # 数据库文件是word.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect(db_path)
    # 创建一个Cursor:
    cursor = conn.cursor()
    with open("db/word.sql", "r", encoding="GBK") as f_r:
        f = f_r.read()
    # 执行一条SQL语句，创建表:
    cursor.executescript(f)
    # cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
    # 继续执行一条SQL语句，插入一条记录:
    # cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
    # 通过rowcount获得插入的行数:
    row = cursor.rowcount
    print(row)
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()


def insert_data(sql):
    """修改数据"""
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        # 执行sql
        response = cursor.execute(sql)
        cursor.close()
        # 提交事务:
        conn.commit()
        return response
    except Exception as e:
        logging.warning('Exception:%s' % e)
    finally:
        conn.close()


def select_data(sql):
    """查询数据"""
    # cursor.execute('select * from word where id=?', ('1',))
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        # 执行sql
        cursor.execute(sql)
        response = cursor.fetchall()
        cursor.close()
        return response
    except Exception as e:
        logging.warning('Exception:%s' % e)
    finally:
        conn.close()


if __name__ == '__main__':
    """创建表"""
    create_table()
