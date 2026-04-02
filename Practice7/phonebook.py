import psycopg2
import csv


conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("Contact added.")


def update_contact():
    old_name = input("Enter the name of contact to update: ")
    new_name = input("Enter new name: ")
    new_phone = input("Enter new phone: ")

    cur.execute(
        "UPDATE phonebook SET name = %s, phone = %s WHERE name = %s",
        (new_name, new_phone, old_name)
    )
    conn.commit()
    print("Contact updated.")


def search_contact():
    print("1 - Search by name")
    print("2 - Search by phone prefix")
    choice = input("Choose: ")

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE name = %s",
            (name,)
        )
    elif choice == "2":
        prefix = input("Enter phone prefix: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (prefix + "%",)
        )
    else:
        print("Invalid choice.")
        return

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")


def delete_contact():
    choice = input("Delete by 1-name or 2-phone: ")

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "DELETE FROM phonebook WHERE name = %s",
            (name,)
        )
    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute(
            "DELETE FROM phonebook WHERE phone = %s",
            (phone,)
        )
    else:
        print("Invalid choice.")
        return

    conn.commit()
    print("Contact deleted.")


def insert_from_csv():
    file_name = input("Enter CSV file name: ")

    with open(file_name, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            name, phone = row
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (name, phone)
            )

    conn.commit()
    print("Contacts inserted from CSV.")


def show_all_contacts():
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("Phonebook is empty.")


while True:
    print("\nPHONEBOOK MENU")
    print("1. Insert from console")
    print("2. Update contact")
    print("3. Search contact")
    print("4. Delete contact")
    print("5. Insert from CSV")
    print("6. Show all contacts")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        insert_from_console()
    elif choice == "2":
        update_contact()
    elif choice == "3":
        search_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        insert_from_csv()
    elif choice == "6":
        show_all_contacts()
    elif choice == "0":
        break
    else:
        print("Invalid choice.")

cur.close()
conn.close()