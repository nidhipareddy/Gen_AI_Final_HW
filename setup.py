#!/usr/bin/env python3
"""
Setup script for Multi-Agent Customer Service System
Automates database setup and verification
"""

import os
import sys
import subprocess


def check_python_version():
    """Verify Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f" Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def setup_database():
    """Run database setup script."""
    print("\n Setting up database...")
    try:
        from database_setup import DatabaseSetup
        import sqlite3
        
        db = DatabaseSetup('support.db')
        db.connect()
        db.create_tables()
        db.create_triggers()
        db.insert_sample_data()
        
        # Add customer 12345 for test scenarios
        db.cursor.execute("""
            INSERT OR IGNORE INTO customers (id, name, email, phone, status)
            VALUES (12345, 'Premium Customer', 'premium@example.com', '+1-555-9999', 'active')
        """)
        db.cursor.execute("""
            INSERT INTO tickets (customer_id, issue, status, priority)
            VALUES (12345, 'Account upgrade request', 'open', 'medium')
        """)
        db.conn.commit()
        db.close()
        
        print(" Database setup complete")
        return True
    except Exception as e:
        print(f" Database setup failed: {e}")
        return False


def test_mcp_tools():
    """Test MCP tools."""
    print("\n Testing MCP tools...")
    try:
        from mcp_tools import MCPTools
        
        tools = MCPTools()
        
        # Quick test
        result = tools.get_customer(5)
        if 'name' in result:
            print(f" MCP tools working - Found customer: {result['name']}")
            return True
        else:
            print(" MCP tools test failed")
            return False
    except Exception as e:
        print(f" MCP tools test failed: {e}")
        return False


def test_agents():
    """Test agent coordination."""
    print("\n Testing agent coordination...")
    try:
        from agents import RouterAgent
        
        router = RouterAgent()
        result = router.route_query("Get customer information for ID 5")
        
        if result and 'final_message' in result:
            print(" Agent coordination working")
            return True
        else:
            print(" Agent coordination test failed")
            return False
    except Exception as e:
        print(f" Agent coordination test failed: {e}")
        return False


def display_summary():
    """Display setup summary and next steps."""
    print("\n" + "="*70)
    print(" SETUP COMPLETE!")
    print("="*70)
    print("\nYour multi-agent customer service system is ready!\n")
    
    print(" Files created:")
    print("   - support.db (SQLite database with 16 customers, 26 tickets)")
    print("   - database_setup.py (Database schema and setup)")
    print("   - mcp_tools.py (5 MCP tools)")
    print("   - agents.py (Router, Customer Data, Support agents)")
    
    print("\n Quick start commands:")
    print("   - Test MCP tools:        python mcp_tools.py")
    print("   - Test agents:           python agents.py")
    print("   - View database:         sqlite3 support.db '.tables'")
    
    print("\n See README.md for detailed documentation")
    print("="*70 + "\n")


def main():
    """Run complete setup."""
    print("="*70)
    print("Multi-Agent Customer Service System - Setup")
    print("="*70)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    # Run setup steps
    steps = [
        ("Database", setup_database),
        ("MCP Tools", test_mcp_tools),
        ("Agents", test_agents),
    ]
    
    failed = []
    for name, func in steps:
        if not func():
            failed.append(name)
    
    if failed:
        print(f"\n Setup incomplete. Failed: {', '.join(failed)}")
        sys.exit(1)
    
    # Display summary
    display_summary()


if __name__ == "__main__":
    main()
