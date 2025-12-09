"""
MCP Tools for Customer Service System
Part 2: MCP Integration

Implements 5 required MCP tools:
1. get_customer(customer_id) - uses customers.id
2. list_customers(status, limit) - uses customers.status
3. update_customer(customer_id, data) - uses customers fields
4. create_ticket(customer_id, issue, priority) - uses tickets fields
5. get_customer_history(customer_id) - uses tickets.customer_id
"""

import sqlite3
import json
from typing import Optional, Dict, List, Any


class MCPTools:
    """MCP tools for accessing customer database."""
    
    def __init__(self, db_path: str = "support.db"):
        """Initialize MCP tools with database path.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
    
    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        """Get customer information by ID.
        
        MCP Tool 1: Uses customers.id
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Customer data as dictionary
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, email, phone, status, created_at, updated_at
            FROM customers
            WHERE id = ?
        """, (customer_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return {"error": f"Customer {customer_id} not found"}
    
    def list_customers(self, status: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List customers with optional status filter.
        
        MCP Tool 2: Uses customers.status
        
        Args:
            status: Filter by status ('active' or 'disabled'), None for all
            limit: Maximum number of customers to return
            
        Returns:
            List of customer data dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT id, name, email, phone, status, created_at, updated_at
                FROM customers
                WHERE status = ?
                LIMIT ?
            """, (status, limit))
        else:
            cursor.execute("""
                SELECT id, name, email, phone, status, created_at, updated_at
                FROM customers
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def update_customer(self, customer_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update customer information.
        
        MCP Tool 3: Uses customers fields
        
        Args:
            customer_id: Customer ID to update
            data: Dictionary of fields to update (name, email, phone, status)
            
        Returns:
            Updated customer data or error
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build UPDATE query dynamically
        allowed_fields = ['name', 'email', 'phone', 'status']
        update_fields = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_fields:
            conn.close()
            return {"error": "No valid fields to update"}
        
        set_clause = ", ".join([f"{field} = ?" for field in update_fields.keys()])
        values = list(update_fields.values()) + [customer_id]
        
        try:
            cursor.execute(f"""
                UPDATE customers
                SET {set_clause}
                WHERE id = ?
            """, values)
            
            conn.commit()
            
            if cursor.rowcount == 0:
                conn.close()
                return {"error": f"Customer {customer_id} not found"}
            
            conn.close()
            return {
                "success": True,
                "customer_id": customer_id,
                "updated_fields": list(update_fields.keys())
            }
        except sqlite3.Error as e:
            conn.close()
            return {"error": str(e)}
    
    def create_ticket(self, customer_id: int, issue: str, priority: str = "medium") -> Dict[str, Any]:
        """Create a new support ticket.
        
        MCP Tool 4: Uses tickets fields
        
        Args:
            customer_id: Customer ID
            issue: Description of the issue
            priority: Priority level ('low', 'medium', 'high')
            
        Returns:
            Created ticket data or error
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Validate priority
        if priority not in ['low', 'medium', 'high']:
            conn.close()
            return {"error": f"Invalid priority: {priority}"}
        
        try:
            cursor.execute("""
                INSERT INTO tickets (customer_id, issue, priority, status)
                VALUES (?, ?, ?, 'open')
            """, (customer_id, issue, priority))
            
            ticket_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "ticket_id": ticket_id,
                "customer_id": customer_id,
                "issue": issue,
                "priority": priority,
                "status": "open"
            }
        except sqlite3.Error as e:
            conn.close()
            return {"error": str(e)}
    
    def get_customer_history(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all tickets for a customer.
        
        MCP Tool 5: Uses tickets.customer_id
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List of ticket data dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, customer_id, issue, status, priority, created_at
            FROM tickets
            WHERE customer_id = ?
            ORDER BY created_at DESC
        """, (customer_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]


def test_mcp_tools():
    """Test all MCP tools."""
    
    tools = MCPTools()
    
    print("\n" + "="*70)
    print("TESTING MCP TOOLS")
    print("="*70)
    
    # Test 1: get_customer
    print("\n1. get_customer(5):")
    result = tools.get_customer(5)
    print(json.dumps(result, indent=2))
    
    # Test 2: list_customers
    print("\n2. list_customers(status='active', limit=3):")
    result = tools.list_customers(status='active', limit=3)
    print(json.dumps(result, indent=2))
    
    # Test 3: update_customer
    print("\n3. update_customer(1, {'email': 'newemail@test.com'}):")
    result = tools.update_customer(1, {'email': 'newemail@test.com'})
    print(json.dumps(result, indent=2))
    
    # Test 4: create_ticket
    print("\n4. create_ticket(5, 'Test ticket', 'high'):")
    result = tools.create_ticket(5, 'Test ticket', 'high')
    print(json.dumps(result, indent=2))
    
    # Test 5: get_customer_history
    print("\n5. get_customer_history(1):")
    result = tools.get_customer_history(1)
    print(json.dumps(result, indent=2))
    
    print("\n" + "="*70)
    print("ALL MCP TOOLS TESTED")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_mcp_tools()
