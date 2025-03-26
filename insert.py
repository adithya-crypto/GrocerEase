import csv
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="grocery_db",
    user="postgres",
    password="a8a3s2s9a1m0",
    host="localhost",
    port="5432",
)

# Open the CSV file and create a CSV reader
with open("grocery_list.csv", "r") as csvfile:
    reader = csv.reader(csvfile)

    # Skip the header row if needed
    next(reader)

    # Iterate over each row in the CSV file
    for row in reader:
        # Extract data from the row
        item = row[0]  # Assuming the item name is in the first column
        price = float(row[1])  # Assuming the price is in the second column

        # Create a cursor object to execute SQL queries
        cur = conn.cursor()

        # Execute an SQL INSERT statement to insert the data into the database table
        cur.execute(
            "INSERT INTO grocery_list (item, price) VALUES (%s, %s)", (item, price)
        )

        # Commit the transaction
        conn.commit()

        # Close the cursor
        cur.close()

# Close the database connection
conn.close()

print("Data inserted successfully!")
