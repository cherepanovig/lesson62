# Домашнее задание по теме "План написания админ панели".
# Цель: написать простейшие CRUD функции для взаимодействия с базой данных.

import sqlite3

def initiate_db(): # создаём таблицу Products, если она ещё не создана при помощи SQL запроса
    connection = sqlite3.connect('data_products.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER
    )
    ''')
    connection.commit()  # сохраняем состояние
    connection.close()  # закрываем соединение

initiate_db()

# def insert_products(): # Заполняем базу4-мя записями
#     connection = sqlite3.connect('data_products.db')
#     cursor = connection.cursor()
#     for i in range(1, 5):
#         cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
#                        (f"Продукт {i}", f"Описание {i}", i*100))
#
#     connection.commit()  # сохраняем состояние
#     connection.close()  # закрываем соединение
#
# insert_products()

# def delete_records(): # Удаляем записи с id с 5 по 16
#     connection = sqlite3.connect('data_products.db')
#     cursor = connection.cursor()
#     cursor.execute("DELETE FROM Products WHERE id BETWEEN 5 AND 16")
#     connection.commit() # сохраняем состояние
#     connection.close() # закрываем соединение
#
# delete_records()

def get_all_products(): # возвращаем все записи из таблицы Products, полученные при помощи SQL запроса.
    connection = sqlite3.connect('data_products.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    for product in products:
        id, title, description, price = product  # Распаковываем кортеж
        print(f"ID: {id} | Наименование: {title} | Описание: {description} | Цена: {price}")

    connection.close()  # закрываем соединение
    return products

#get_all_products()



# connection.commit() # сохраняем состояние
# connection.close() # закрываем соединение