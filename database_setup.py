"""
Database Setup for Multi-Agent Customer Service System
Creates SQLite database with customers and tickets tables
Includes sample data for testing
"""

import sqlite3
from datetime import datetime, timedelta
import random


class DatabaseSetup:
    """Initialize and populate the customer service database"""
    
    def __init__(self, db_path="support.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def create_tables(self):
        """Create customers and tickets tables"""
        cursor = self.conn.cursor()
        
        # Drop existing tables
        cursor.execute('DROP TABLE IF EXISTS tickets')
        cursor.execute('DROP TABLE IF EXISTS customers')
        
        # Create customers table
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create tickets table
        cursor.execute('''
            CREATE TABLE tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                issue TEXT NOT NULL,
                status TEXT DEFAULT 'open',
                priority TEXT DEFAULT 'medium',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        self.conn.commit()
        print("✅ Tables created successfully")
    
    def insert_sample_customers(self):
        """Insert sample customer data"""
        cursor = self.conn.cursor()
        
        customers = [
            ('Alice Johnson', 'alice.johnson@email.com', '+1-555-0101', 'active'),
            ('Bob Smith', 'bob.smith@email.com', '+1-555-0102', 'active'),
            ('Carol White', 'carol.white@email.com', '+1-555-0103', 'active'),
            ('David Brown', 'david.brown@email.com', '+1-555-0104', 'disabled'),
            ('Charlie Brown', 'charlie.brown@email.com', '+1-555-0105', 'active'),
            ('Eve Davis', 'eve.davis@email.com', '+1-555-0106', 'active'),
            ('Frank Miller', 'frank.miller@email.com', '+1-555-0107', 'active'),
            ('Grace Lee', 'grace.lee@email.com', '+1-555-0108', 'disabled'),
            ('Henry Wilson', 'henry.wilson@email.com', '+1-555-0109', 'active'),
            ('Iris Martinez', 'iris.martinez@email.com', '+1-555-0110', 'active'),
        ]
        
        cursor.executemany(
            'INSERT INTO customers (name, email, phone, status) VALUES (?, ?, ?, ?)',
            customers
        )
        
        self.conn.commit()
        print(f"✅ Inserted {len(customers)} sample customers")
    
    def insert_sample_tickets(self):
        """Insert sample ticket data"""
        cursor = self.conn.cursor()
        
        issues = [
            "Cannot login to account",
            "Billing discrepancy on last invoice",
            "Feature request: dark mode",
            "Password reset not working",
            "Account upgrade inquiry",
            "Charged twice for subscription",
            "Cannot access premium features",
            "Email notifications not received",
            "Data export request",
            "Account deletion request",
            "Performance issues with dashboard",
            "Integration with third-party service",
            "Mobile app crashes on startup",
            "Cannot change payment method",
            "Refund request for unused service"
        ]
        
        statuses = ['open', 'in_progress', 'resolved']
        priorities = ['low', 'medium', 'high']
        
        tickets = []
        for i in range(15):
            customer_id = random.randint(1, 10)
            issue = issues[i]
            status = random.choice(statuses)
            priority = random.choice(priorities)
            tickets.append((customer_id, issue, status, priority))
        
        cursor.executemany(
            'INSERT INTO tickets (customer_id, issue, status, priority) VALUES (?, ?, ?, ?)',
            tickets
        )
        
        self.conn.commit()
        print(f"✅ Inserted {len(tickets)} sample tickets")
    
    def verify_data(self):
        """Verify database contents"""
        cursor = self.conn.cursor()
        
        # Count customers
        cursor.execute('SELECT COUNT(*) as count FROM customers')
        customer_count = cursor.fetchone()['count']
        print(f"✅ Total customers: {customer_count}")
        
        # Count active customers
        cursor.execute("SELECT COUNT(*) as count FROM customers WHERE status='active'")
        active_count = cursor.fetchone()['count']
        print(f"✅ Active customers: {active_count}")
        
        # Count tickets
        cursor.execute('SELECT COUNT(*) as count FROM tickets')
        ticket_count = cursor.fetchone()['count']
        print(f"✅ Total tickets: {ticket_count}")
        
        # Count by status
        cursor.execute('SELECT status, COUNT(*) as count FROM tickets GROUP BY status')
        for row in cursor.fetchall():
            print(f"   - {row['status']}: {row['count']}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    """Main setup function"""
    print("="*70)
    print("DATABASE SETUP - Multi-Agent Customer Service System")
    print("="*70)
    
    db = DatabaseSetup('support.db')
    
    try:
        # Connect to database
        db.connect()
        print("\n1. Creating tables...")
        db.create_tables()
        
        print("\n2. Inserting sample customers...")
        db.insert_sample_customers()
        
        print("\n3. Inserting sample tickets...")
        db.insert_sample_tickets()
        
        print("\n4. Verifying data...")
        db.verify_data()
        
        print("\n" + "="*70)
        print("✅ DATABASE SETUP COMPLETE!")
        print("="*70)
        print(f"\nDatabase file: support.db")
        print("Ready to use with MCP Server and agents")
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
