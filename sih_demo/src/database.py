import sqlite3
from datetime import datetime

DB_PATH = "procurement.db"

def init_db():
    """Initializes the database tables if they do not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            crop TEXT NOT NULL,
            quantity_quintals REAL NOT NULL,
            booking_date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            status TEXT DEFAULT 'Confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_slot_availability(booking_date, time_slot, max_capacity=10):
    """Checks how many slots are left for a given date and time slot."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM bookings 
        WHERE booking_date = ? AND time_slot = ?
    """, (booking_date, time_slot))
    count = cursor.fetchone()[0]
    conn.close()
    return max(0, max_capacity - count)

def add_booking(farmer_name, phone, crop, quantity, booking_date, time_slot):
    """Registers a new drop-off booking."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (farmer_name, phone, crop, quantity_quintals, booking_date, time_slot)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (farmer_name, phone, crop, quantity, booking_date, time_slot))
    conn.commit()
    booking_id = cursor.lastrowid
    conn.close()
    return booking_id

def get_farmer_bookings(phone):
    """Fetches all bookings associated with a phone number."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, crop, quantity_quintals, booking_date, time_slot, status 
        FROM bookings 
        WHERE phone = ? 
        ORDER BY id DESC
    """, (phone,))
    records = cursor.fetchall()
    conn.close()
    return records

def update_booking_status(booking_id, new_status):
    """Admin function to update a token's status (e.g., 'Processing', 'Completed')."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (new_status, booking_id))
    conn.commit()
    conn.close()

def get_live_queue_stats(booking_date, time_slot, current_booking_id):
    """Calculates the current live token and how many tokens are ahead of the farmer."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Find which token is currently being processed at the mandi
    cursor.execute("""
        SELECT id FROM bookings 
        WHERE booking_date = ? AND time_slot = ? AND status = 'Processing' 
        LIMIT 1
    """, (booking_date, time_slot))
    processing_record = cursor.fetchone()
    live_token = processing_record[0] if processing_record else "None currently processing"
    
    # 2. Count how many 'Confirmed' tokens are ahead of the user in this time slot
    cursor.execute("""
        SELECT COUNT(*) FROM bookings 
        WHERE booking_date = ? AND time_slot = ? AND status = 'Confirmed' AND id < ?
    """, (booking_date, time_slot, current_booking_id))
    people_ahead = cursor.fetchone()[0]
    
    conn.close()
    return live_token, people_ahead