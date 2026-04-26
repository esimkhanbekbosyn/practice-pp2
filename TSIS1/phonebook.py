import csv        
import json         
from connect import connect  


# SQL файлды оқып, database-та орындау
def run_sql_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

    print(f"{filename} executed successfully.")


# Database table-дар мен procedure/function жасау
def setup_database():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")


# Group бар ма тексереді, жоқ болса жасайды, сосын group id қайтарады
def get_group_id(cur, group_name):
    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]



def add_contact():
    name = input("Name: ")
    surname = input("Surname: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_name = input("Group: ")

    phone = input("Phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    if birthday == "":
        birthday = None

    with connect() as conn:
        with conn.cursor() as cur:
            group_id = get_group_id(cur, group_name)

            # contact қосамыз
            cur.execute("""
                INSERT INTO contacts(name, surname, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (name, surname, email, birthday, group_id))

            # жаңа contact id аламыз
            contact_id = cur.fetchone()[0]

            # сол contact-қа phone қосамыз
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, phone_type))

    print("Contact added.")


# Барлық contact-тарды шығару
def show_all():
    with connect() as conn:
        with conn.cursor() as cur:
            # contacts + groups + phones table-дарын JOIN арқылы қосамыз
            cur.execute("""
                SELECT c.name, c.surname, c.email, c.birthday,
                       g.name, p.phone, p.type, c.created_at
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON p.contact_id = c.id
                ORDER BY c.id
            """)

            rows = cur.fetchall()

            for row in rows:
                print(row)


# Existing contact-қа жаңа phone қосу
def add_phone_console():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    with connect() as conn:
        with conn.cursor() as cur:
            # Database procedure шақырамыз
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    print("Phone added.")


# Contact-ты басқа group-қа ауыстыру
def move_to_group_console():
    name = input("Contact name: ")
    group_name = input("New group: ")

    with connect() as conn:
        with conn.cursor() as cur:
            # Database procedure шақырамыз
            cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

    print("Contact moved.")


# Name, surname, email, phone, group бойынша search
def search_console():
    query = input("Search: ")

    with connect() as conn:
        with conn.cursor() as cur:
            # Database function шақырамыз
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = cur.fetchall()

            for row in rows:
                print(row)


# Group бойынша filter
def filter_by_group():
    group_name = input("Group name: ")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, c.surname, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON p.contact_id = c.id
                WHERE g.name = %s
            """, (group_name,))

            for row in cur.fetchall():
                print(row)


# Email ішінде partial search жасау
def search_by_email():
    email_part = input("Email search: ")

    with connect() as conn:
        with conn.cursor() as cur:
            # ILIKE үлкен/кіші әріпке қарамай іздейді
            cur.execute("""
                SELECT name, surname, email, birthday
                FROM contacts
                WHERE email ILIKE %s
            """, (f"%{email_part}%",))

            for row in cur.fetchall():
                print(row)


# Contact-тарды name, birthday немесе created_at бойынша sort жасау
def sort_contacts():
    print("1 - name")
    print("2 - birthday")
    print("3 - date added")

    choice = input("Choose sort: ")

    if choice == "1":
        order = "c.name"
    elif choice == "2":
        order = "c.birthday"
    elif choice == "3":
        order = "c.created_at"
    else:
        print("Wrong choice")
        return

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT c.name, c.surname, c.email, c.birthday, g.name, c.created_at
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                ORDER BY {order}
            """)

            for row in cur.fetchall():
                print(row)


# Pagination: contact-тарды page-page қылып шығару
def pagination_console():
    limit = 3      # бір page-та 3 contact
    offset = 0     # қай жерден бастаймыз

    while True:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT name, surname, email, birthday
                    FROM contacts
                    ORDER BY id
                    LIMIT %s OFFSET %s
                """, (limit, offset))

                rows = cur.fetchall()

                print("\nPAGE")
                for row in rows:
                    print(row)

        command = input("n-next, p-prev, q-quit: ")

        if command == "n":
            offset += limit
        elif command == "p":
            offset = max(0, offset - limit)
        elif command == "q":
            break


# Database-тағы contact-тарды JSON файлға шығару
def export_json():
    data = []

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.name, c.surname, c.email, c.birthday, g.name
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                ORDER BY c.id
            """)

            contacts = cur.fetchall()

            for contact in contacts:
                contact_id, name, surname, email, birthday, group_name = contact

                cur.execute("""
                    SELECT phone, type
                    FROM phones
                    WHERE contact_id = %s
                """, (contact_id,))

                phones = cur.fetchall()

                data.append({
                    "name": name,
                    "surname": surname,
                    "email": email,
                    "birthday": str(birthday) if birthday else None,
                    "group": group_name,
                    "phones": [
                        {"phone": p[0], "type": p[1]}
                        for p in phones
                    ]
                })

    # JSON файлға жазамыз
    with open("contacts_export.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("Exported to contacts_export.json")


# JSON файлдан database-қа contact қосу
def import_json():
    filename = input("JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    with connect() as conn:
        with conn.cursor() as cur:
            for item in data:
                name = item["name"]

                # Contact already exists па тексереміз
                cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                existing = cur.fetchone()

                if existing:
                    action = input(f"{name} already exists. skip/overwrite: ")

                    if action == "skip":
                        continue

                    if action == "overwrite":
                        contact_id = existing[0]
                        group_id = get_group_id(cur, item["group"])

                       
                        cur.execute("""
                            UPDATE contacts
                            SET surname=%s, email=%s, birthday=%s, group_id=%s
                            WHERE id=%s
                        """, (
                            item["surname"],
                            item["email"],
                            item["birthday"],
                            group_id,
                            contact_id
                        ))

                    
                        cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

                else:
                    group_id = get_group_id(cur, item["group"])

                    
                    cur.execute("""
                        INSERT INTO contacts(name, surname, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    """, (
                        item["name"],
                        item["surname"],
                        item["email"],
                        item["birthday"],
                        group_id
                    ))

                    contact_id = cur.fetchone()[0]

                
                for phone in item["phones"]:
                    cur.execute("""
                        INSERT INTO phones(contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (contact_id, phone["phone"], phone["type"]))

    print("JSON imported.")


# CSV файлдан contacts import жасау
def import_csv():
    filename = input("CSV filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        with connect() as conn:
            with conn.cursor() as cur:
                for row in reader:
                    # group id аламыз немесе group жасаймыз
                    group_id = get_group_id(cur, row["group"])

                    # contact insert немесе already exists болса update
                    cur.execute("""
                        INSERT INTO contacts(name, surname, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (name) DO UPDATE
                        SET surname = EXCLUDED.surname,
                            email = EXCLUDED.email,
                            birthday = EXCLUDED.birthday,
                            group_id = EXCLUDED.group_id
                        RETURNING id
                    """, (
                        row["name"],
                        row["surname"],
                        row["email"],
                        row["birthday"],
                        group_id
                    ))

                    contact_id = cur.fetchone()[0]

                    # phone insert
                    cur.execute("""
                        INSERT INTO phones(contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (
                        contact_id,
                        row["phone"],
                        row["phone_type"]
                    ))

    print("CSV imported.")


# Негізгі menu
def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1 - Setup database")
        print("2 - Add contact")
        print("3 - Show all contacts")
        print("4 - Add phone")
        print("5 - Move contact to group")
        print("6 - Search contacts")
        print("7 - Filter by group")
        print("8 - Search by email")
        print("9 - Sort contacts")
        print("10 - Pagination")
        print("11 - Export JSON")
        print("12 - Import JSON")
        print("13 - Import CSV")
        print("0 - Exit")

        choice = input("Choose: ")

        # User таңдаған option бойынша функция шақырылады
        if choice == "1":
            setup_database()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            show_all()
        elif choice == "4":
            add_phone_console()
        elif choice == "5":
            move_to_group_console()
        elif choice == "6":
            search_console()
        elif choice == "7":
            filter_by_group()
        elif choice == "8":
            search_by_email()
        elif choice == "9":
            sort_contacts()
        elif choice == "10":
            pagination_console()
        elif choice == "11":
            export_json()
        elif choice == "12":
            import_json()
        elif choice == "13":
            import_csv()
        elif choice == "0":
            break
        else:
            print("Wrong choice.")



if __name__ == "__main__":
    menu()