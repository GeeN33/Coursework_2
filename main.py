import psycopg2
import os
from dotenv import load_dotenv, find_dotenv
import json

def parsing_address(address:str) -> dict:
    """
    Разбирает адрес на страну город адрес

    """
    dict_temp = {}
    list_address = address.split(';')
    dict_temp["country"] = list_address[0].strip()
    if list_address[1] == ' ':
        address_temp = list_address[2]
        for i in range(4, len(list_address)):
            address_temp += ','+list_address[i]
        dict_temp["address"] = address_temp.strip()
        dict_temp["city"] = list_address[3].strip()
    else:
        address_temp = ''
        for i in range(2, len(list_address)):
            address_temp += list_address[i]
        dict_temp["address"] = address_temp.strip()
        dict_temp["city"] = list_address[1].strip()
    return  dict_temp

def parsing_json(list_suppliers:list, dict_products:dict)->None:
    """
    Разбирает suppliers.json на suppliers и products

    """
    with open('suppliers.json', 'r') as fp:
        data = json.load(fp)
    i= 0
    for d in data:
        i += 1
        dict_temp = {}
        dict_temp_address = parsing_address(d["address"])
        dict_temp["id"] = i
        dict_temp["company_name"] = d["company_name"].replace("'", "''")
        dict_temp["contact"] = d["contact"]
        dict_temp["country"] = dict_temp_address["country"]
        dict_temp["city"] = dict_temp_address["city"]
        dict_temp["address"] = dict_temp_address["address"].replace("'", "''")
        dict_temp["phone"] = d["phone"]
        dict_temp["fax"] = d["fax"]
        dict_temp["homepage"] = d["homepage"].replace("'", "''")
        list_suppliers.append(dict_temp)

        for p in d['products']:
            dict_products[p] = i

def filling_db(connection)->None:
    """
     заполнение БД
    """
    with open('Northwind_Traders_Sql.sql', 'r') as fp:
        command = fp.read()
    request(connection, command)
    print('БД заполнена')

def db_connect():
    """
     Соединяется с базой данных
    :return: соединение
    """
    try:
        load_dotenv(find_dotenv())
        connection = psycopg2.connect(host= os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'), database=os.getenv('db_name'))
        connection.autocommit = True
        print('connection')
        return connection

    except Exception as ex:
        print(ex)
        return False

def request(connection, command:str) -> None:
    """
    Отправляет SQL команды в базу данных
    :param Соединение:
    :param SQL команды:
    :return:
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(command)
            return cursor.fetchall()
    except Exception as ex:
        return ex

def print_rez(rez,name_table:str) -> None:
    """
     Выводит таблицу
    :param rez:Данные из базы
    """
    if type(rez) == list:
        for r in rez:
            print(r)
    elif str(rez) == 'no results to fetch':
        print('create_table: '+ name_table)
    else: print(rez)

def create_table(connection)->None:
    """
    Создаёт таблицу
    """
    command = """
        CREATE TABLE IF NOT EXISTS suppliers
        (
        id serial PRIMARY KEY,
        company_name varchar(100),
        contact varchar(100),
        country varchar(50),
        city varchar(50),
        address varchar(100),      
        phone varchar(50),
        fax varchar(50),
        homepage varchar(100)    
        )
        """
    rez = request(connection, command)
    print_rez(rez,'suppliers')

def add_column_products(connection)->None:
    """
     Добавляет колонку fk_suppliers  в products
    """
    command = """
        ALTER TABLE products 
        ADD COLUMN fk_suppliers int REFERENCES suppliers(id)
        """
    request(connection, command)
    print('Колонка добавлена fk_suppliers  в products ')

def insert_into_suppliers(connection, list_suppliers:list)->None:
    """
    Добавляет данные в таблицу  suppliers
    """
    try:
        with connection.cursor() as cursor:

            for  v in list_suppliers:
                q = f"""
                    INSERT INTO suppliers (id, company_name, contact, country, city, address, phone, fax, homepage)

                    VALUES ('{v['id']}','{v['company_name']}','{v['contact']}','{v['country']}','{v['city']}','{v['address']}','{v['phone']}','{v['fax']}','{v['homepage']}')
                    """
                cursor.execute(q)
            print('Заполнена таблица suppliers')
    except Exception as ex:
        print(ex)

def update_set_fk_products(connection, dict_products:dict)->None:
    """
    Заполняет столбец fk_suppliers в таблице products данными из словаря  dict_products
    """
    try:
        with connection.cursor() as cursor:

            for  k, v in dict_products.items():
                tk = k.replace("'", "''")
                q = f"""
                    UPDATE products
                    SET fk_suppliers = '{v}'
                    WHERE product_name = '{tk}'
                    
                    """
                cursor.execute(q)
            print('update_set_fk_products')
    except Exception as ex:
        print(ex)
def name():

    dict_products = {}
    list_suppliers = []
    parsing_json(list_suppliers, dict_products)
    connection = db_connect()
    if not connection:
        print('нет соединения с базой данных')
        return
    filling_db(connection)
    create_table(connection)
    insert_into_suppliers(connection, list_suppliers)
    add_column_products(connection)
    update_set_fk_products(connection, dict_products)

    if connection:
         connection.close()


if __name__ == '__main__':
    name()
