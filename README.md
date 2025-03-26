# GrocerEase: Grocery Bill Generator

A desktop application for generating grocery bills with automatic item suggestions, price calculations, and PDF receipts.

## Overview

GrocerEase is a Python-based desktop application designed to streamline the process of creating grocery bills. It features a user-friendly interface with auto-complete functionality for item entry, delivery options, and PDF bill generation. The application connects to a PostgreSQL database to retrieve item information and prices.

## Features

- **Item Auto-completion**: As you type, the system suggests grocery items from the database
- **Dynamic Pricing**: Automatically retrieves prices from the database
- **Delivery Options**: Choose between pickup or delivery (with $6 delivery fee)
- **Customer Information**: Include customer details for better record-keeping
- **Payment Method Selection**: Support for multiple payment methods (Zelle, Cash)
- **PDF Bill Generation**: Creates professional PDF receipts with complete order details
- **Database Integration**: Connects to PostgreSQL for data storage and retrieval

## Tech Stack

- **Frontend**: Python with Tkinter for GUI
- **Backend**: Python with PostgreSQL integration
- **Database**: PostgreSQL
- **PDF Generation**: FPDF library

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Required Python packages (see requirements.txt)

### Setup

1. Clone the repository
   ```
   git clone https://github.com/yourusername/GrocerEase.git
   cd GrocerEase
   ```

2. Install required packages
   ```
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database
   ```
   createdb grocery_db
   ```

4. Create the grocery_list table in your PostgreSQL database:
   ```sql
   CREATE TABLE grocery_list (
     id SERIAL PRIMARY KEY,
     item VARCHAR(255) NOT NULL,
     price DECIMAL(10, 2) NOT NULL
   );
   ```

5. Import your grocery items (optional)
   ```
   python insert.py
   ```

## Usage

1. Start the application
   ```
   python frontend.py
   ```

2. Enter item names in the first field (auto-completion will suggest items)

3. Enter quantities in the second field

4. Click "Add Item" to add items to the bill

5. Select delivery option and enter customer information if needed

6. Choose payment method

7. Click "Generate Bill" to create a PDF receipt

## Database Management

- To add a new item to the database:
  ```
  python insert_item.py
  ```

- To import items from a CSV file:
  ```
  python insert.py
  ```

## File Structure

- `frontend.py`: The main application UI and event handling
- `backend.py`: Database operations and PDF generation
- `insert.py`: Script to import items from a CSV file
- `insert_item.py`: Script to add individual items to the database
- `grocery_list.csv`: Sample grocery items and prices

## Security Note

This repository contains database credentials that should be secured before deployment. For production use, it's recommended to:

1. Move database credentials to environment variables or a config file
2. Add the config file to .gitignore to prevent accidental exposure

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- FPDF library for PDF generation
- PostgreSQL for reliable data storage
- Tkinter for the GUI components
