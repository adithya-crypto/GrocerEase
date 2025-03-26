# backend.py
import psycopg2
from fpdf import FPDF
from decimal import Decimal


def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname="grocery_db",
            user="postgres",
            password="a8a3s2s9a1m0",
            host="localhost",
            port="5432",
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None


def fetch_item_suggestions(conn, prefix):
    suggestions = []
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT item FROM grocery_list WHERE item ILIKE %s OR item ILIKE %s OR item ILIKE %s",
            (
                "%" + prefix + "%",
                "%" + prefix,
                prefix + "%",
            ),
        )
        rows = cur.fetchall()
        for row in rows:
            suggestions.append(row[0])
    except psycopg2.Error as e:
        print("Error fetching item suggestions:", e)
    return suggestions


def fetch_item_price(conn, item):
    try:
        cur = conn.cursor()
        cur.execute("SELECT price FROM grocery_list WHERE item ILIKE %s", (item,))
        row = cur.fetchone()
        if row:
            return row[0]
        else:
            return 0  # Return zero if item not found in the database
    except psycopg2.Error as e:
        print("Error fetching item price:", e)
        return None


def generate_pdf_bill(
    conn,
    order_number,
    items,
    delivery_option,
    customer_name,
    customer_phone,
    customer_address,
    payment_method,
):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Order No: {order_number}", ln=True, align="L")

    if customer_name:
        pdf.cell(
            200,
            10,
            txt=f"Customer Info: {customer_name}, Phone: {customer_phone}, Address: {customer_address}",
            ln=True,
            align="L",
        )
        pdf.cell(200, 10, txt=f"Payment Method: {payment_method}", ln=True, align="L")

    pdf.set_fill_color(200, 220, 255)
    pdf.cell(60, 10, "Item", 1, 0, "C", 1)
    pdf.cell(30, 10, "Quantity", 1, 0, "C", 1)
    pdf.cell(30, 10, "Price", 1, 0, "C", 1)
    pdf.cell(40, 10, "Total", 1, 1, "C", 1)

    total_cost = Decimal(0)
    for item, quantity in items.items():
        price = fetch_item_price(conn, item)
        if price is not None:
            total_item_cost = price * Decimal(quantity)
            total_cost += total_item_cost
            pdf.cell(60, 10, item, 1)
            pdf.cell(30, 10, str(quantity), 1, 0, "C")
            pdf.cell(30, 10, str(price), 1, 0, "C")
            pdf.cell(40, 10, str(total_item_cost), 1, 1, "C")
        else:
            total_cost += Decimal(0)

    if delivery_option == "Delivery":
        total_cost += 6
        pdf.cell(60, 10, "Delivery", 1)
        pdf.cell(30, 10, "", 1)  # Empty cell for Quantity
        pdf.cell(30, 10, "6", 1)  # Delivery amount
        pdf.cell(40, 10, "", 1)  # Empty cell for Total
        pdf.ln()  # Move to the next line after delivery row
    else:
        pdf.cell(200, 10, "", 0, 1)  # Empty cell for alignment

    pdf.cell(80, 10, "Total", 1, 0, "C")
    pdf.cell(
        80, 10, str(total_cost), 1, 1, "C"
    )  # Move to the next line after printing total

    pdf_output = f"bill_{order_number}.pdf"
    pdf.output(pdf_output)

    return pdf_output
