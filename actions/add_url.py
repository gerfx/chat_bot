import sqlite3


def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS MEALS
                 (id INT AUTO_INCREMENT, meal_name VARCHAR(100), meal_url VARCHAR(100))''')
    cursor.execute("CREATE TABLE IF NOT EXISTS User (user_id integer, meal_id integer)")


def insert_words(file, cursor):
    words = file.readlines()

    for word in words:
        cursor.execute("INSERT INTO Meals (id, meal_name) VALUES (?, ?)", (word.split(': ')))


def write():
    with open("recipes.txt", "r") as recipes,  sqlite3.connect("recipes.db") as conn:
        cursor = conn.cursor()

        create_tables(cursor)

        insert_words(recipes, cursor)
        conn.commit()


if __name__ == "__main__":
    write()
