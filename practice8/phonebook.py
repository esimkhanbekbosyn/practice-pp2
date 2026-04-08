from connect import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            surname VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def create_functions_and_procedures():
    conn = get_connection()
    cur = conn.cursor()

    # functions.sql
    with open("functions.sql", "r", encoding="utf-8") as f:
        cur.execute(f.read())

    # procedures.sql
    with open("procedures.sql", "r", encoding="utf-8") as f:
        cur.execute(f.read())

    conn.commit()
    cur.close()
    conn.close()


def upsert_contact(name, surname, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s, %s);", (name, surname, phone))

    conn.commit()
    cur.close()
    conn.close()


def search_contacts(pattern):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def get_paginated_contacts(limit, offset):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s);", (value,))

    conn.commit()
    cur.close()
    conn.close()


def insert_many_contacts(names, surnames, phones):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_many_contacts(%s, %s, %s);",
        (names, surnames, phones)
    )

    # incorrect_data temp table-ден оқу
    cur.execute("SELECT * FROM incorrect_data;")
    incorrect_rows = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return incorrect_rows


def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts ORDER BY id;")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def main():
    create_table()
    create_functions_and_procedures()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Upsert contact")
        print("2. Search by pattern")
        print("3. Insert many contacts")
        print("4. Get paginated contacts")
        print("5. Delete contact by name or phone")
        print("6. Show all contacts")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            name = input("Enter name: ")
            surname = input("Enter surname: ")
            phone = input("Enter phone: ")

            upsert_contact(name, surname, phone)
            print("Contact inserted or updated.")

        elif choice == "2":
            pattern = input("Enter pattern: ")
            rows = search_contacts(pattern)

            if rows:
                for row in rows:
                    print(row)
            else:
                print("No matches found.")

        elif choice == "3":
            n = int(input("How many contacts do you want to add? "))

            names = []
            surnames = []
            phones = []

            for i in range(n):
                print(f"\nContact {i + 1}:")
                names.append(input("Name: "))
                surnames.append(input("Surname: "))
                phones.append(input("Phone: "))

            incorrect = insert_many_contacts(names, surnames, phones)

            print("Bulk insert finished.")
            if incorrect:
                print("Incorrect data:")
                for row in incorrect:
                    print(row)
            else:
                print("All data inserted correctly.")

        elif choice == "4":
            limit = int(input("Enter limit: "))
            offset = int(input("Enter offset: "))

            rows = get_paginated_contacts(limit, offset)
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No records found.")

        elif choice == "5":
            value = input("Enter username or phone to delete: ")
            delete_contact(value)
            print("Delete procedure completed.")

        elif choice == "6":
            rows = show_all_contacts()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("PhoneBook is empty.")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()