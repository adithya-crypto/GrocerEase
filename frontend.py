import _tkinter as tk
from _tkinter import messagebox
import backend
import random


def handle_item_entry(event):
    prefix = entry_item.get()
    suggestions = backend.fetch_item_suggestions(conn, prefix)
    autocomplete_listbox.delete(0, tk.END)
    for suggestion in suggestions:
        autocomplete_listbox.insert(tk.END, suggestion)


def handle_item_selection(event):
    if autocomplete_listbox.curselection():
        selected_item = autocomplete_listbox.get(autocomplete_listbox.curselection())
        entry_item.delete(0, tk.END)
        entry_item.insert(tk.END, selected_item)
        entry_item.focus_set()


def add_item():
    item = entry_item.get()
    quantity = entry_quantity.get()
    if item and quantity:
        items_listbox.insert(tk.END, f"{item} - {quantity}")
        entry_item.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)


def delete_item():
    selected_index = items_listbox.curselection()
    if selected_index:
        items_listbox.delete(selected_index)


def generate_bill():
    order_number = "INDFLA" + str(random.randint(10000, 99999))
    items = {}
    for i in range(items_listbox.size()):
        item, quantity = items_listbox.get(i).split(" - ")
        items[item] = float(quantity)  # Convert quantity to float

    delivery_option = var_delivery.get()
    customer_name = entry_customer.get()
    customer_phone = entry_phone.get()
    customer_address = entry_address.get()
    payment_method = var_payment_method.get()
    pdf_url = backend.generate_pdf_bill(
        conn,
        order_number,
        items,
        delivery_option,
        customer_name,
        customer_phone,
        customer_address,
        payment_method,
    )
    messagebox.showinfo(
        "Success", f"Bill generated successfully! PDF saved as {pdf_url}"
    )


root = tk.Tk()
root.title("Grocery Bill Generator")

conn = backend.connect_to_database()
if conn:
    print("Connected to the database successfully!")
else:
    print("Failed to connect to the database.")


entry_item = tk.Entry(root)
entry_item.grid(row=0, column=0, padx=10, pady=5)
entry_item.bind("<KeyRelease>", handle_item_entry)


autocomplete_listbox = tk.Listbox(root)
autocomplete_listbox.grid(row=1, column=0, padx=10, pady=5)
autocomplete_listbox.bind("<<ListboxSelect>>", handle_item_selection)

entry_quantity = tk.Entry(root)
entry_quantity.grid(row=0, column=2, padx=10, pady=5)


btn_add_item = tk.Button(root, text="Add Item", command=add_item)
btn_add_item.grid(row=0, column=3, padx=10, pady=5)

btn_delete_item = tk.Button(root, text="Delete Item", command=delete_item)
btn_delete_item.grid(row=1, column=3, padx=10, pady=5)

items_listbox = tk.Listbox(root)
items_listbox.grid(row=1, column=2, columnspan=1, padx=10, pady=5)

var_delivery = tk.StringVar()
var_delivery.set("Pickup")
rb_pickup = tk.Radiobutton(root, text="Pickup", variable=var_delivery, value="Pickup")
rb_pickup.grid(row=3, column=0, padx=10, pady=5)
rb_delivery = tk.Radiobutton(
    root, text="Delivery (+$6)", variable=var_delivery, value="Delivery"
)
rb_delivery.grid(row=3, column=1, padx=10, pady=5)

label_customer = tk.Label(root, text="Customer Name:")
label_customer.grid(row=4, column=0, padx=10, pady=5)
entry_customer = tk.Entry(root)
entry_customer.grid(row=4, column=1, padx=10, pady=5)

label_phone = tk.Label(root, text="Phone Number:")
label_phone.grid(row=5, column=0, padx=10, pady=5)
entry_phone = tk.Entry(root)
entry_phone.grid(row=5, column=1, padx=10, pady=5)

label_address = tk.Label(root, text="Address:")
label_address.grid(row=6, column=0, padx=10, pady=5)
entry_address = tk.Entry(root)
entry_address.grid(row=6, column=1, padx=10, pady=5)

label_payment_method = tk.Label(root, text="Payment Method:")
label_payment_method.grid(row=7, column=0, padx=10, pady=5)
var_payment_method = tk.StringVar()
payment_methods = ["Zelle", "Cash"]
payment_option_menu = tk.OptionMenu(root, var_payment_method, *payment_methods)
payment_option_menu.grid(row=7, column=1, padx=10, pady=5)

btn_generate_bill = tk.Button(root, text="Generate Bill", command=generate_bill)
btn_generate_bill.grid(row=8, columnspan=3, padx=10, pady=5)

root.mainloop()
