from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
DB_NAME = "car_booking.db"

# Helper function to connect to the database
def connect_db():
    return sqlite3.connect(DB_NAME)

# Routes for general pages
@app.route('/')
def index():
    return render_template('index.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash('Login successful!')
            return redirect(url_for('customer_dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        conn = connect_db()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
        if cursor.fetchone():
            flash('An account with this email already exists')
            conn.close()
            return render_template('register.html')
        
        cursor.execute("""
            INSERT INTO customers (name, email, phone, password)
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, password))
        
        conn.commit()
        conn.close()
        
        flash('Registration successful! You can now login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('index'))

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            flash('Admin login successful!')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials')
    
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        flash('Please login as admin first')
        return redirect(url_for('admin_login'))
    
    return render_template('admin/dashboard.html')

@app.route('/admin/bookings')
def admin_bookings():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, cu.name, c.brand, c.model, c.price, b.booking_date, b.delivery_date
        FROM bookings b
        JOIN customers cu ON b.customer_id = cu.id
        JOIN cars c ON b.car_id = c.id
        ORDER BY b.booking_date DESC
    """)
    bookings = cursor.fetchall()
    conn.close()
    
    return render_template('admin/bookings.html', bookings=bookings)

@app.route('/admin/analytics')
def admin_analytics():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Most booked models
    cursor.execute("""
        SELECT c.brand, c.model, COUNT(*) as count
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        GROUP BY b.car_id
        ORDER BY count DESC
        LIMIT 5
    """)
    top_models = cursor.fetchall()
    
    # Bookings by brand
    cursor.execute("""
        SELECT c.brand, COUNT(*) as count
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        GROUP BY c.brand
        ORDER BY count DESC
    """)
    brand_bookings = cursor.fetchall()
    
    # Total revenue
    cursor.execute("""
        SELECT SUM(c.price)
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
    """)
    total_revenue = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return render_template('admin/analytics.html', 
                          top_models=top_models, 
                          brand_bookings=brand_bookings,
                          total_revenue=total_revenue)

# Customer routes
@app.route('/dashboard')
def customer_dashboard():
    if not session.get('user_id'):
        flash('Please login first')
        return redirect(url_for('login'))
    
    return render_template('customer/dashboard.html', user_name=session.get('user_name'))

@app.route('/cars')
def car_selection():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Get all brands
    cursor.execute("SELECT DISTINCT brand FROM cars")
    brands = [row[0] for row in cursor.fetchall()]
    
    # Get featured cars
    cursor.execute("""
        SELECT id, brand, model, price, bhp, top_speed
        FROM cars
        ORDER BY price DESC
        LIMIT 6
    """)
    featured_cars = cursor.fetchall()
    
    conn.close()
    
    return render_template('customer/car_selection.html', 
                          brands=brands, 
                          featured_cars=featured_cars)

@app.route('/cars/<brand>')
def car_by_brand(brand):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, model, price, bhp, torque, top_speed, mileage
        FROM cars
        WHERE brand = ?
    """, (brand,))
    cars = cursor.fetchall()
    conn.close()
    
    return render_template('customer/brand_cars.html', brand=brand, cars=cars)

@app.route('/car/<int:car_id>')
def car_details(car_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
    car = cursor.fetchone()
    conn.close()
    
    if not car:
        flash('Car not found')
        return redirect(url_for('car_selection'))
    
    return render_template('customer/car_details.html', car=car)

@app.route('/book/<int:car_id>', methods=['GET', 'POST'])
def book_car(car_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
    car = cursor.fetchone()
    conn.close()
    
    if not car:
        flash('Car not found')
        return redirect(url_for('car_selection'))
    
    if request.method == 'POST':
        # Process payment
        booking_date = datetime.now()
        delivery_date = booking_date + timedelta(days=90)
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings (customer_id, car_id, booking_date, delivery_date)
            VALUES (?, ?, ?, ?)
        """, (session['user_id'], car_id, booking_date.date(), delivery_date.date()))
        conn.commit()
        conn.close()
        
        flash('Booking confirmed! Your car will be delivered on ' + delivery_date.strftime('%Y-%m-%d'))
        return redirect(url_for('booking_history'))
    
    return render_template('customer/payment.html', car=car)

@app.route('/bookings')
def booking_history():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, b.booking_date, b.delivery_date, c.brand, c.model, c.price
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        WHERE b.customer_id = ?
        ORDER BY b.booking_date DESC
    """, (session['user_id'],))
    bookings = cursor.fetchall()
    
    today = datetime.now().date()
    formatted_bookings = []
    
    for booking in bookings:
        bid, book_date, delivery_date, brand, model, price = booking
        book_date = datetime.strptime(book_date, "%Y-%m-%d").date()
        delivery_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()
        days_left = (delivery_date - today).days
        status = "Delivered" if days_left <= 0 else "Pending"
        
        formatted_bookings.append({
            'id': bid,
            'brand': brand,
            'model': model,
            'price': price,
            'booking_date': book_date,
            'delivery_date': delivery_date,
            'status': status,
            'days_left': days_left
        })
    
    conn.close()
    
    return render_template('customer/booking_history.html', bookings=formatted_bookings)

@app.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Get booking details
    cursor.execute("""
        SELECT customer_id, car_id, booking_date 
        FROM bookings 
        WHERE id = ?
    """, (booking_id,))
    booking = cursor.fetchone()
    
    if not booking or booking[0] != session['user_id']:
        flash('Invalid booking')
        conn.close()
        return redirect(url_for('booking_history'))
    
    # Record cancellation
    cancellation_date = datetime.now().date()
    cursor.execute("""
        INSERT INTO cancellations (customer_id, car_id, booking_date, cancellation_date)
        VALUES (?, ?, ?, ?)
    """, (booking[0], booking[1], booking[2], cancellation_date))
    
    # Delete booking
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    
    conn.commit()
    conn.close()
    
    flash('Booking successfully cancelled')
    return redirect(url_for('booking_history'))

if __name__ == '__main__':
    app.run(debug=True)
