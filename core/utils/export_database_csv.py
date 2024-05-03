import csv
import sqlite3


def export_csv():  # Подключение к базе данных SQLite
    conn = sqlite3.connect('lot.db')
    cursor = conn.cursor()
    # Выполнить SQL-запрос
    query = "SELECT * FROM users"
    cursor.execute(query)
    data = cursor.fetchall()
    # Записать данные в CSV-файл
    with open('users.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Write header
        writer.writerows(data)  # Write data rows
    # Закрыть подключение к базе
    conn.close()
