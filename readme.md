# Car Booking System (React Frontend + Flask Backend)
![Project Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Tech Stack](https://img.shields.io/badge/stack-React%20%2B%20Flask%20%2B%20SQLite-blueviolet)
## Overview

The Car Booking System is a full-stack application with a React.js frontend and Flask backend using SQLite. It simulates a real-world car booking workflow where users can register, log in, browse available cars, make bookings, and view their history. Admin users can access analytics and manage bookings.

## 🚀 Features

### User
- Register and log in
- Select a car brand and view available models
- View detailed specifications of each model
- Simulated payment screen for booking
- View booking history and cancellation records

### Admin
- View all bookings and user data
- Track booking status
- Analytics on bookings and brands

## ⚙️ Tech Stack
- **Frontend**: React.js, TailwindCSS, ShadCN UI
- **Backend**: Python 3.x, Flask
- **Database**: SQLite3

## 📂 Project Structure
```
car_booking_system/
├── backend/
│   ├── app.py
│   ├── initialize_db.py
│   ├── car_booking.db
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   ├── tailwind.config.js
│   └── package.json
```

## 🧱 Database Schema
- **cars**: id, brand, model, cc, bhp, torque, transmission, top_speed, mileage, tank_capacity, seats, price
- **customers**: id, name, email, password
- **bookings**: id, customer_id, car_id, booking_date, delivery_date, status
- **cancellations**: id, booking_id, cancel_date

## 🛠 Setup Instructions

### Backend
1. Navigate to the backend directory:
```bash
cd backend
```
2. Install dependencies:
```bash
pip install flask
```
3. Initialize the database:
```bash
python initialize_db.py
```
4. Run the Flask app:
```bash
python app.py
```

### Frontend
1. Navigate to the frontend directory:
```bash
cd frontend
```
2. Install dependencies:
```bash
npm install
```
3. Run the React app:
```bash
npm run dev
```

## 🔐 Authentication
- Customers register with email and password.
- Admin credentials can be hardcoded (e.g., `admin`/`admin123`).

## 📊 Admin Dashboard Features
- View all bookings
- Booking and cancellation statistics
- Revenue analytics

## 📌 Notes
- React UI is responsive and styled with Tailwind and ShadCN.
- Flask APIs communicate with React via REST endpoints.
- SQLite file (`car_booking.db`) stores all persistent data.

---
This project is modular, extensible, and ideal for demonstration of full-stack development with authentication, CRUD operations, and basic analytics.
