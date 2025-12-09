"""
MCP Server Implementation - Flask with JSON-RPC
Provides 5 tools for customer service operations
Runs on port 5000 with /mcp endpoint
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime


class MCPServer:
    """MCP Server providing customer service tools via HTTP JSON-RPC"""
    
    def __init__(self, db_path='support.db', port=5000):
        """
        Initialize MCP Server
        
        Args:
            db_path: Path to SQLite database
            port: Port to run Flask server on
        """
        self.db_path = db_path
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Setup routes
        self._setup_routes()
    
    def _get_db_connection(self):
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ========================================================================
    # MCP TOOL IMPLEMENTATIONS
    # ========================================================================
    
    def get_customer(self, customer_id: int):
        """
        Get customer information by ID
        
        Args:
            customer_id: Customer ID to retrieve
            
        Returns:
            dict: Customer data or error
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'success': True,
                    'customer': {
                        'id': row['id'],
                        'name': row['name'],
                        'email': row['email'],
                        'phone': row['phone'],
                        'status': row['status'],
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'Customer {customer_id} not found'
                }
        finally:
            conn.close()
    
    def list_customers(self, status: str = 'active', limit: int = 100):
        """
        List customers filtered by status
        
        Args:
            status: Filter by status ('active' or 'disabled')
            limit: Maximum number of results
            
        Returns:
            dict: List of customers
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT * FROM customers WHERE status = ? ORDER BY id LIMIT ?',
                (status, limit)
            )
            rows = cursor.fetchall()
            
            customers = []
            for row in rows:
                customers.append({
                    'id': row['id'],
                    'name': row['name'],
                    'email': row['email'],
                    'phone': row['phone'],
                    'status': row['status']
                })
            
            return {
                'success': True,
                'count': len(customers),
                'customers': customers
            }
        finally:
            conn.close()
    
    def update_customer(self, customer_id: int, data: dict):
        """
        Update customer information
        
        Args:
            customer_id: Customer ID to update
            data: Dictionary with fields to update
            
        Returns:
            dict: Success status
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Build update query
            updates = []
            values = []
            
            allowed_fields = ['name', 'email', 'phone', 'status']
            for field in allowed_fields:
                if field in data:
                    updates.append(f'{field} = ?')
                    values.append(data[field])
            
            if not updates:
                return {
                    'success': False,
                    'error': 'No valid fields to update'
                }
            
            # Add updated_at timestamp
            updates.append('updated_at = ?')
            values.append(datetime.now().isoformat())
            
            # Add customer_id for WHERE clause
            values.append(customer_id)
            
            query = f"UPDATE customers SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            return {
                'success': cursor.rowcount > 0,
                'customer_id': customer_id,
                'updated_fields': list(data.keys())
            }
        finally:
            conn.close()
    
    def create_ticket(self, customer_id: int, issue: str, priority: str = 'medium'):
        """
        Create a new support ticket
        
        Args:
            customer_id: Customer ID
            issue: Ticket description
            priority: Priority level ('low', 'medium', 'high')
            
        Returns:
            dict: New ticket information
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Validate customer exists
            cursor.execute('SELECT id FROM customers WHERE id = ?', (customer_id,))
            if not cursor.fetchone():
                return {
                    'success': False,
                    'error': f'Customer {customer_id} not found'
                }
            
            # Create ticket
            cursor.execute(
                'INSERT INTO tickets (customer_id, issue, status, priority) VALUES (?, ?, ?, ?)',
                (customer_id, issue, 'open', priority)
            )
            ticket_id = cursor.lastrowid
            conn.commit()
            
            return {
                'success': True,
                'ticket_id': ticket_id,
                'customer_id': customer_id,
                'issue': issue,
                'priority': priority,
                'status': 'open'
            }
        finally:
            conn.close()
    
    def get_customer_history(self, customer_id: int):
        """
        Get all tickets for a customer
        
        Args:
            customer_id: Customer ID
            
        Returns:
            dict: List of customer's tickets
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT * FROM tickets WHERE customer_id = ? ORDER BY created_at DESC',
                (customer_id,)
            )
            rows = cursor.fetchall()
            
            tickets = []
            for row in rows:
                tickets.append({
                    'id': row['id'],
                    'customer_id': row['customer_id'],
                    'issue': row['issue'],
                    'status': row['status'],
                    'priority': row['priority'],
                    'created_at': row['created_at']
                })
            
            return {
                'success': True,
                'customer_id': customer_id,
                'ticket_count': len(tickets),
                'tickets': tickets
            }
        finally:
            conn.close()
    
    # ========================================================================
    # FLASK ROUTES
    # ========================================================================
    
    def _setup_routes(self):
        """Setup Flask routes for MCP protocol"""
        
        @self.app.route('/mcp', methods=['POST'])
        def mcp_endpoint():
            """Main MCP JSON-RPC endpoint"""
            try:
                data = request.json
                method = data.get('method')
                params = data.get('params', {})
                req_id = data.get('id')
                
                # Handle tools/list request
                if method == 'tools/list':
                    return jsonify({
                        'jsonrpc': '2.0',
                        'id': req_id,
                        'result': {
                            'tools': [
                                {
                                    'name': 'get_customer',
                                    'description': 'Get customer information by customer ID',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'customer_id': {
                                                'type': 'integer',
                                                'description': 'The customer ID to look up'
                                            }
                                        },
                                        'required': ['customer_id']
                                    }
                                },
                                {
                                    'name': 'list_customers',
                                    'description': 'List customers filtered by status',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'status': {
                                                'type': 'string',
                                                'enum': ['active', 'disabled'],
                                                'default': 'active'
                                            },
                                            'limit': {
                                                'type': 'integer',
                                                'default': 100
                                            }
                                        }
                                    }
                                },
                                {
                                    'name': 'update_customer',
                                    'description': 'Update customer information',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'customer_id': {
                                                'type': 'integer'
                                            },
                                            'data': {
                                                'type': 'object',
                                                'properties': {
                                                    'name': {'type': 'string'},
                                                    'email': {'type': 'string'},
                                                    'phone': {'type': 'string'},
                                                    'status': {'type': 'string', 'enum': ['active', 'disabled']}
                                                }
                                            }
                                        },
                                        'required': ['customer_id', 'data']
                                    }
                                },
                                {
                                    'name': 'create_ticket',
                                    'description': 'Create a new support ticket',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'customer_id': {
                                                'type': 'integer'
                                            },
                                            'issue': {
                                                'type': 'string'
                                            },
                                            'priority': {
                                                'type': 'string',
                                                'enum': ['low', 'medium', 'high'],
                                                'default': 'medium'
                                            }
                                        },
                                        'required': ['customer_id', 'issue']
                                    }
                                },
                                {
                                    'name': 'get_customer_history',
                                    'description': 'Get all support tickets for a customer',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'customer_id': {
                                                'type': 'integer'
                                            }
                                        },
                                        'required': ['customer_id']
                                    }
                                }
                            ]
                        }
                    })
                
                # Handle tools/call request
                elif method == 'tools/call':
                    tool_name = params.get('name')
                    arguments = params.get('arguments', {})
                    
                    # Map tool names to methods
                    tools_map = {
                        'get_customer': self.get_customer,
                        'list_customers': self.list_customers,
                        'update_customer': self.update_customer,
                        'create_ticket': self.create_ticket,
                        'get_customer_history': self.get_customer_history
                    }
                    
                    if tool_name in tools_map:
                        try:
                            result = tools_map[tool_name](**arguments)
                            return jsonify({
                                'jsonrpc': '2.0',
                                'id': req_id,
                                'result': {
                                    'content': [
                                        {
                                            'type': 'text',
                                            'text': json.dumps(result)
                                        }
                                    ]
                                }
                            })
                        except Exception as e:
                            return jsonify({
                                'jsonrpc': '2.0',
                                'id': req_id,
                                'error': {
                                    'code': -32603,
                                    'message': f'Tool execution error: {str(e)}'
                                }
                            }), 500
                    else:
                        return jsonify({
                            'jsonrpc': '2.0',
                            'id': req_id,
                            'error': {
                                'code': -32601,
                                'message': f'Unknown tool: {tool_name}'
                            }
                        }), 404
                
                return jsonify({'error': 'Invalid method'}), 400
                
            except Exception as e:
                return jsonify({
                    'error': f'Server error: {str(e)}'
                }), 500
        
        @self.app.route('/health', methods=['GET'])
        def health():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'server': 'mcp-server',
                'version': '1.0'
            })
    
    def run(self, debug=False):
        """
        Run the Flask server
        
        Args:
            debug: Enable debug mode
        """
        print(f"🚀 Starting MCP Server on http://localhost:{self.port}")
        print(f"   Endpoint: http://localhost:{self.port}/mcp")
        print(f"   Health: http://localhost:{self.port}/health")
        self.app.run(host='127.0.0.1', port=self.port, debug=debug, use_reloader=False)


def main():
    """Run MCP Server standalone"""
    server = MCPServer(db_path='support.db', port=5000)
    server.run(debug=False)


if __name__ == "__main__":
    main()
