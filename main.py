import sqlite3
from getpass import getpass
from datetime import datetime, timedelta
import sys
DB_NAME = "car_booking.db"


def launch():
    while True:
        print("\n--- Welcome to Car Booking System ---")
        print("1. Customer Login/Register")
        print("2. Admin Login")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            customer_id = main_menu()
            if customer_id:
                customer_dashboard(customer_id)
        elif choice == "2":
            if admin_login():
                admin_dashboard()
        elif choice == "3":
            print("Exiting system.")
            sys.exit()
        else:
            print("Invalid input.")

def admin_login():
    print("\n--- Admin Login ---")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == "admin" and password == "admin123":
        print("Login successful.")
        return True
    else:
        print("Invalid credentials.")
        return False

def admin_dashboard():
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. View all bookings")
        print("2. View all cancellations")
        print("3. View total revenue")
        print("4. View analytics")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_all_bookings()
        elif choice == "2":
            view_all_cancellations()
        elif choice == "3":
            view_total_revenue()
        elif choice == "4":
            view_admin_analytics()
        elif choice == "5":
            print("Logging out from admin...")
            break
        else:
            print("Invalid input.")

def view_admin_analytics():
    print("\n--- Admin Analytics ---")
    print("1. Most booked car models")
    print("2. Booking count by brand")
    print("3. Monthly booking trends")
    print("4. Back")

    choice = input("Enter your choice: ")

    if choice == "1":
        most_booked_models()
    elif choice == "2":
        bookings_by_brand()
    elif choice == "3":
        monthly_booking_trends()
    elif choice == "4":
        return
    else:
        print("Invalid input.")


def view_all_bookings():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.id, cu.name, c.brand, c.model, c.price, b.booking_date, b.delivery_date
        FROM bookings b
        JOIN customers cu ON b.customer_id = cu.id
        JOIN cars c ON b.car_id = c.id
        ORDER BY b.booking_date DESC
    """)
    
    records = cursor.fetchall()
    conn.close()

    print("\n--- All Bookings ---")
    for idx, (bid, cust_name, brand, model, price, book_date, delivery_date) in enumerate(records, start=1):
        print(f"\n#{idx}")
        print(f"Customer: {cust_name}")
        print(f"Car: {brand} {model}")
        print(f"Price: ${price}")
        print(f"Booking Date: {book_date}")
        print(f"Delivery Date: {delivery_date}")

def most_booked_models():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.brand, c.model, COUNT(*) as count
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        GROUP BY b.car_id
        ORDER BY count DESC
        LIMIT 5
    """)
    records = cursor.fetchall()
    conn.close()

    print("\n--- Most Booked Car Models ---")
    for idx, (brand, model, count) in enumerate(records, start=1):
        print(f"{idx}. {brand} {model} - {count} bookings")

        
def bookings_by_brand():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.brand, COUNT(*) as count
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        GROUP BY c.brand
        ORDER BY count DESC
    """)
    records = cursor.fetchall()
    conn.close()

    print("\n--- Bookings by Brand ---")
    for brand, count in records:
        print(f"{brand}: {count} bookings")
def monthly_booking_trends():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%Y-%m', booking_date) as month, COUNT(*) as count
        FROM bookings
        GROUP BY month
        ORDER BY month
    """)
    records = cursor.fetchall()
    conn.close()

    print("\n--- Monthly Booking Trends ---")
    for month, count in records:
        print(f"{month}: {count} bookings")

def view_all_cancellations():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT x.id, cu.name, c.brand, c.model, c.price, x.booking_date, x.cancellation_date
        FROM cancellations x
        JOIN customers cu ON x.customer_id = cu.id
        JOIN cars c ON x.car_id = c.id
        ORDER BY x.cancellation_date DESC
    """)
    
    records = cursor.fetchall()
    conn.close()

    print("\n--- All Cancellations ---")
    for idx, (cid, cust_name, brand, model, price, book_date, cancel_date) in enumerate(records, start=1):
        print(f"\n#{idx}")
        print(f"Customer: {cust_name}")
        print(f"Car: {brand} {model}")
        print(f"Price: ${price}")
        print(f"Booking Date: {book_date}")
        print(f"Cancellation Date: {cancel_date}")
def view_total_revenue():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(c.price)
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
    """)
    revenue = cursor.fetchone()[0]
    conn.close()

    print(f"\nTotal Revenue from Bookings: ${revenue if revenue else 0}")

def connect_db():
    return sqlite3.connect(DB_NAME)

def register():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n--- Customer Registration ---")
    name = input("Enter full name: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    password = getpass("Create a password: ")

    # Check if email already exists
    cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
    if cursor.fetchone():
        print("An account with this email already exists. Try logging in.")
        return

    cursor.execute("""
        INSERT INTO customers (name, email, phone, password)
        VALUES (?, ?, ?, ?)
    """, (name, email, phone, password))

    conn.commit()
    conn.close()
    print("Registration successful. You can now login.")

def login():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n--- Customer Login ---")
    email = input("Enter email: ")
    password = getpass("Enter password: ")

    cursor.execute("SELECT * FROM customers WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        print(f"Welcome back, {user[1]}!")
        return user[0]  # return customer ID
    else:
        print("Invalid credentials. Please try again.")
        return None

def main_menu():
    while True:
        print("\n====== Car Booking System ======")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            customer_id = login()
            if customer_id:
                return customer_id  # Proceed to car selection
        elif choice == "2":
            register()
        elif choice == "3":
            print("Exiting application.")
            exit()
        else:
            print("Invalid input. Please choose 1, 2, or 3.")

def get_brands():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT brand FROM cars")
    brands = [row[0] for row in cursor.fetchall()]

    conn.close()
    return brands

def get_models_by_brand(brand):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, model FROM cars WHERE brand = ?", (brand,))
    models = cursor.fetchall()

    conn.close()
    return models

def get_car_details(car_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
    car = cursor.fetchone()

    conn.close()
    return car

def choose_car(customer_id):
    print("\n--- Available Brands ---")
    brands = get_brands()
    for idx, brand in enumerate(brands, start=1):
        print(f"{idx}. {brand}")

    while True:
        try:
            brand_choice = int(input("Select a brand by number: "))
            if 1 <= brand_choice <= len(brands):
                selected_brand = brands[brand_choice - 1]
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

    models = get_models_by_brand(selected_brand)
    if not models:
        print("No models available for this brand.")
        return None

    print(f"\n--- Models Available in {selected_brand} ---")
    for idx, (car_id, model) in enumerate(models, start=1):
        print(f"{idx}. {selected_brand} {model}")

    while True:
        try:
            model_choice = int(input("Select a model by number: "))
            if 1 <= model_choice <= len(models):
                selected_car_id = models[model_choice - 1][0]
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

    car = get_car_details(selected_car_id)

    print("\n--- Car Specifications ---")
    fields = ["ID", "Model", "Brand", "CC", "BHP", "Torque", "Transmission", "Top Speed", "Mileage", "Tank Capacity", "Seats", "Price ($)"]
    for label, value in zip(fields, car):
        print(f"{label}: {value}")
    
    # Ask for confirmation before proceeding
    while True:
        confirm = input("\nDo you want to proceed with this car? (Y/N): ").strip().lower()
        if confirm == 'y':
            return car  # Proceed to payment
        elif confirm == 'n':
            print("Let's select again.")
            return choose_car(customer_id)  # Restart brand/model selection
        else:
            print("Please enter Y or N.")

    return car  # Return selected car record

def simulate_payment_and_book(customer_id, car):
    print("\n--- Payment Portal ---")
    card_number = input("Enter your card number: ")
    pin = input("Enter your card PIN: ")

    if len(card_number) < 4 or len(pin) < 2:
        print("Invalid card details. Booking cancelled.")
        return

    print("Processing payment...")
    # Simulate a delay (optional)
    # time.sleep(1)

    # Calculate delivery date (3 months from now)
    booking_date = datetime.now()
    delivery_date = booking_date + timedelta(days=90)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings (customer_id, car_id, booking_date, delivery_date)
        VALUES (?, ?, ?, ?)
    """, (customer_id, car[0], booking_date.date(), delivery_date.date()))

    conn.commit()
    conn.close()

    print("\n--- Booking Confirmed ---")
    print(f"Car: {car[2]} {car[1]}")
    print(f"Price: ${car[11]}")
    print(f"Booking Date: {booking_date.date()}")
    print(f"Expected Delivery Date: {delivery_date.date()}")


def view_booking_history(customer_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.booking_date, b.delivery_date, c.brand, c.model, c.price
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        WHERE b.customer_id = ?
        ORDER BY b.booking_date DESC
    """, (customer_id,))
    
    records = cursor.fetchall()
    conn.close()

    if not records:
        print("\nNo bookings found.")
        return

    print("\n--- Booking History ---")
    today = datetime.now().date()

    for idx, (book_date, delivery_date, brand, model, price) in enumerate(records, start=1):
        book_date = datetime.strptime(book_date, "%Y-%m-%d").date()
        delivery_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()

        days_left = (delivery_date - today).days
        status = "Delivered" if days_left <= 0 else "Pending"
        days_display = "Delivered" if days_left <= 0 else f"{days_left} days remaining"

        print(f"\nBooking #{idx}")
        print(f"Car: {brand} {model}")
        print(f"Price: ${price}")
        print(f"Booking Date: {book_date}")
        print(f"Delivery Date: {delivery_date}")
        print(f"Delivery Status: {status}")
        print(f"Time Left: {days_display}")

def cancel_booking(customer_id):
    conn = connect_db()
    cursor = conn.cursor()

    today = datetime.now().date()

    # Fetch only *pending* bookings
    cursor.execute("""
        SELECT b.id, c.brand, c.model, b.booking_date, b.delivery_date
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        WHERE b.customer_id = ?
        ORDER BY b.booking_date DESC
    """, (customer_id,))
    all_bookings = cursor.fetchall()

    # Filter for pending
    pending = [
        (idx + 1, bid, brand, model, b_date, d_date)
        for idx, (bid, brand, model, b_date, d_date) in enumerate(all_bookings)
        if datetime.strptime(d_date, "%Y-%m-%d").date() > today
    ]

    if not pending:
        print("\nYou have no pending bookings to cancel.")
        conn.close()
        return

    print("\n--- Pending Bookings ---")
    for idx, booking_id, brand, model, book_date, delivery_date in pending:
        print(f"{idx}. {brand} {model} | Booking Date: {book_date} | Delivery Date: {delivery_date}")

    try:
        choice = int(input("\nEnter the number of the booking you want to cancel (0 to exit): "))
        if choice == 0:
            print("Cancellation aborted.")
            return

        if 1 <= choice <= len(pending):
            booking_id = pending[choice - 1][1]
            # Fetch car_id and booking_date for record
            cursor.execute("SELECT customer_id, car_id, booking_date FROM bookings WHERE id = ?", (booking_id,))
            cust_id, car_id, booking_date = cursor.fetchone()
            cancellation_date = datetime.now().date()

            # Insert into cancellations table
            cursor.execute("""
                INSERT INTO cancellations (customer_id, car_id, booking_date, cancellation_date)
                VALUES (?, ?, ?, ?)
            """, (cust_id, car_id, booking_date, cancellation_date))

            # Delete from bookings
            cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
            conn.commit()
            print("Booking successfully cancelled and logged.")

        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")
    finally:
        conn.close()
def view_cancellation_history(customer_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.brand, c.model, x.booking_date, x.cancellation_date, c.price
        FROM cancellations x
        JOIN cars c ON x.car_id = c.id
        WHERE x.customer_id = ?
        ORDER BY x.cancellation_date DESC
    """, (customer_id,))

    records = cursor.fetchall()
    conn.close()

    if not records:
        print("\nNo cancellations found.")
        return

    print("\n--- Cancellation History ---")
    for idx, (brand, model, booking_date, cancellation_date, price) in enumerate(records, start=1):
        print(f"\nCancellation #{idx}")
        print(f"Car: {brand} {model}")
        print(f"Price: ${price}")
        print(f"Booking Date: {booking_date}")
        print(f"Cancellation Date: {cancellation_date}")

# Call entry point
if __name__ == "__main__":
    while True:
        print("\n--- Welcome to Car Booking System ---")
        print("1. Customer Login/Register")
        print("2. Admin Login")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")
        if choice == "1":
            customer_id = main_menu()
            if customer_id:
                while True:
                    print("\n--- What would you like to do? ---")
                    print("1. Book a new car")
                    print("2. View booking history")
                    print("3. Cancel a booking")
                    print("4. View cancellation history")
                    print("5. Logout")

                    user_choice = input("Enter your choice (1-5): ")

                    if user_choice == "1":
                        selected_car = choose_car(customer_id)
                        if selected_car:
                            simulate_payment_and_book(customer_id, selected_car)
                    elif user_choice == "2":
                        view_booking_history(customer_id)
                    elif user_choice == "3":
                        cancel_booking(customer_id)
                    elif user_choice == "4":
                        view_cancellation_history(customer_id)
                    elif user_choice == "5":
                        print("Logging out...")
                        sys.exit()
                    else:
                        print("Invalid input.")
        elif choice == "2":
            if admin_login():
                admin_dashboard()
        elif choice == "3":
            print("Exiting system.")
            break
        else:
            print("Invalid input.")
    