import csv
from connect import connect


def insert_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone, email) VALUES (%s, %s, %s);",
        (name, phone, email)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added!")


def insert_from_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            name, phone, email = row
            cur.execute(
                "INSERT INTO phonebook (name, phone, email) VALUES (%s, %s, %s);",
                (name, phone, email)
            )

    conn.commit()
    cur.close()
    conn.close()

    print("Contacts imported from CSV!")


def show_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()

    if not rows:
        print("PhoneBook is empty.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def search_by_name():
    name = input("Enter name to search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook WHERE name = %s;", (name,))
    rows = cur.fetchall()

    if not rows:
        print("No contacts found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def search_by_prefix():
    prefix = input("Enter phone prefix: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s;", (prefix + "%",))
    rows = cur.fetchall()

    if not rows:
        print("No contacts found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def update_name():
    old_name = input("Enter current name: ")
    new_name = input("Enter new name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET name = %s WHERE name = %s;",
        (new_name, old_name)
    )

    conn.commit()
    print("Updated rows:", cur.rowcount)

    cur.close()
    conn.close()


def update_phone():
    name = input("Enter name: ")
    new_phone = input("Enter new phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s;",
        (new_phone, name)
    )

    conn.commit()
    print("Updated rows:", cur.rowcount)

    cur.close()
    conn.close()


def delete_by_name():
    name = input("Enter name to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE name = %s;", (name,))

    conn.commit()
    print("Deleted rows:", cur.rowcount)

    cur.close()
    conn.close()


def delete_by_phone():
    phone = input("Enter phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE phone = %s;", (phone,))

    conn.commit()
    print("Deleted rows:", cur.rowcount)

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Add contact from console")
        print("2. Import contacts from CSV")
        print("3. Show all contacts")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Update name")
        print("7. Update phone")
        print("8. Delete by name")
        print("9. Delete by phone")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            insert_contact()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            show_all()
        elif choice == "4":
            search_by_name()
        elif choice == "5":
            search_by_prefix()
        elif choice == "6":
            update_name()
        elif choice == "7":
            update_phone()
        elif choice == "8":
            delete_by_name()
        elif choice == "9":
            delete_by_phone()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


menu()