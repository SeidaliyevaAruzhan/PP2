import psycopg2
import json

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")

    cur.execute(
        "INSERT INTO contacts(name, email, birthday) VALUES (%s,%s,%s) RETURNING id",
        (name, email, birthday)
    )
    cid = cur.fetchone()[0]

    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    cur.execute(
        "INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s)",
        (cid, phone, ptype)
    )

    conn.commit()


def add_phone():
    name = input("Name: ")
    phone = input("Phone: ")
    ptype = input("Type: ")

    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))
    conn.commit()


def move_group():
    name = input("Name: ")
    group = input("Group: ")

    cur.execute("CALL move_to_group(%s,%s)", (name, group))
    conn.commit()


def search_all():
    query = input("Search: ")
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    for row in cur.fetchall():
        print(row)


def search_email():
    email = input("Email: ")
    cur.execute("SELECT * FROM contacts WHERE email ILIKE %s", ('%' + email + '%',))
    print(cur.fetchall())


def filter_group():
    group = input("Group: ")
    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))
    print(cur.fetchall())


def sort_contacts():
    ch = input("1-name 2-birthday: ")
    if ch == "1":
        cur.execute("SELECT * FROM contacts ORDER BY name")
    else:
        cur.execute("SELECT * FROM contacts ORDER BY birthday")
    print(cur.fetchall())


def paginate():
    page = 0
    limit = 2
    while True:
        cur.execute("SELECT * FROM get_phonebook_paginated(%s,%s)", (limit, page * limit))
        print(cur.fetchall())
        cmd = input("next / prev / quit: ")
        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        else:
            break


def show_all():
    cur.execute("""
        SELECT c.name, c.email, p.phone
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
    """)
    for row in cur.fetchall():
        print(row)


def export_json():
    cur.execute("""
        SELECT c.name, c.email, p.phone
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
    """)
    data = cur.fetchall()
    with open("contacts.json", "w") as f:
        json.dump(data, f)


def import_json():
    try:
        with open("contacts.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("contacts.json жоқ")
        return

    for name, email, phone in data:
        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input("skip/overwrite: ")
            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute(
            "INSERT INTO contacts(name, email) VALUES (%s,%s) RETURNING id",
            (name, email)
        )
        cid = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO phones(contact_id, phone) VALUES (%s,%s)",
            (cid, phone)
        )

    conn.commit()


while True:
    print("\nMENU")
    print("1 Add contact")
    print("2 Add phone")
    print("3 Move to group")
    print("4 Search (all)")
    print("5 Search by email")
    print("6 Filter by group")
    print("7 Sort")
    print("8 Pagination")
    print("9 Show all")
    print("10 Export JSON")
    print("11 Import JSON")
    print("0 Exit")

    ch = input("Choose: ")

    if ch == "1":
        add_contact()
    elif ch == "2":
        add_phone()
    elif ch == "3":
        move_group()
    elif ch == "4":
        search_all()
    elif ch == "5":
        search_email()
    elif ch == "6":
        filter_group()
    elif ch == "7":
        sort_contacts()
    elif ch == "8":
        paginate()
    elif ch == "9":
        show_all()
    elif ch == "10":
        export_json()
    elif ch == "11":
        import_json()
    elif ch == "0":
        break

cur.close()
conn.close()