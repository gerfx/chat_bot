import os
import sqlite3
import pymorphy2


morph = pymorphy2.MorphAnalyzer()


def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Meals
                 (id INT AUTO_INCREMENT, meal_name VARCHAR(100), meal_url VARCHAR(100))''')
    cursor.execute("CREATE TABLE IF NOT EXISTS User (user_id integer, meal_id integer)")


def insert_words(file, cursor):
    words = file.readlines()

    id_1 = 0
    for word in words:
        p = morph.parse(word.split(': ')[0])[0].normal_form
        cursor.execute("INSERT INTO Meals (id, meal_name, meal_url) VALUES (?, ?, ?)", (id_1, p, word.split(': ')[1]))
        id_1 += 1


def write():
    relative = os.path.join(os.curdir, "recipes.txt")
    absolute_path = os.path.abspath(relative)
    with open(absolute_path, "r") as recipes,  sqlite3.connect("recipes.db") as conn:
        cursor = conn.cursor()

        create_tables(cursor)
        conn.commit()

        insert_words(recipes, cursor)
        conn.commit()

        print()


if __name__ == "__main__":
    write()
