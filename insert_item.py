import psycopg2


def insert_item(conn, item, price):
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO grocery_list (item, price) VALUES (%s, %s)", (item, price)
        )
        conn.commit()
        print("Item inserted successfully!")
    except psycopg2.Error as e:
        print("Error inserting item:", e)


# Example usage
conn = psycopg2.connect(
    dbname="grocery_db",
    user="postgres",
    password="a8a3s2s9a1m0",
    host="localhost",
    port="5432",
)

insert_item(conn, "Sooji Rava 4lb", 5.99)
