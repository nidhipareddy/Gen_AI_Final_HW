"""
Agent Implementations for Multi-Agent Customer Service System
Part 1: System Architecture

Three specialized agents:
1. Router Agent (Orchestrator) - Coordinates queries and routes to specialists
2. Customer Data Agent (Specialist) - Accesses customer database via MCP
3. Support Agent (Specialist) - Handles customer support queries
"""

from typing import Dict, Any, List
from mcp_tools import MCPTools


class CustomerDataAgent:
    """Specialist agent for customer data operations via MCP.
    
    Responsibilities:
    - Access customer database via MCP
    - Retrieve customer information
    - Update customer records
    - Handle data validation
    """
    
    def __init__(self, db_path: str = "support.db"):
        """Initialize Customer Data Agent with MCP tools.
        
        Args:
            db_path: Path to database
        """
        self.name = "Customer Data Agent"
        self.mcp = MCPTools(db_path)
    
    def handle_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle data-related queries using MCP tools.
        
        Args:
            query: Customer data query
            context: Additional context (customer_id, etc.)
            
        Returns:
            Query result
        """
        print(f"   [{self.name}] Processing query: {query[:50]}...")
        
        if not context:
            context = {}
        
        # Route to appropriate MCP tool based on query
        if "customer_id" in context:
            customer_id = context["customer_id"]
            
            if "history" in query.lower() or "tickets" in query.lower():
                print(f"   [{self.name}] Calling MCP: get_customer_history({customer_id})")
                return {"history": self.mcp.get_customer_history(customer_id)}
            else:
                print(f"   [{self.name}] Calling MCP: get_customer({customer_id})")
                return {"customer": self.mcp.get_customer(customer_id)}
        
        elif "list" in query.lower() or "all" in query.lower():
            status = context.get("status", "active")
            limit = context.get("limit", 100)
            print(f"   [{self.name}] Calling MCP: list_customers(status='{status}')")
            return {"customers": self.mcp.list_customers(status, limit)}
        
        elif "update" in query.lower():
            customer_id = context.get("customer_id")
            data = context.get("data", {})
            print(f"   [{self.name}] Calling MCP: update_customer({customer_id}, {data})")
            return {"update_result": self.mcp.update_customer(customer_id, data)}
        
        else:
            return {"error": "Unable to determine data operation"}


class SupportAgent:
    """Specialist agent for customer support.
    
    Responsibilities:
    - Handle general customer support queries
    - Can escalate complex issues
    - Request customer context from Data Agent
    - Provide solutions and recommendations
    """
    
    def __init__(self):
        """Initialize Support Agent."""
        self.name = "Support Agent"
    
    def handle_query(self, query: str, customer_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle support queries with customer context.
        
        Args:
            query: Support query
            customer_data: Customer context from Data Agent
            
        Returns:
            Support response with escalation info if needed
        """
        print(f"   [{self.name}] Analyzing query: {query[:50]}...")
        
        # Detect urgency/escalation triggers
        escalation_keywords = ['charged twice', 'refund', 'immediately', 'urgent', 'cancel']
        needs_escalation = any(keyword in query.lower() for keyword in escalation_keywords)
        
        if needs_escalation:
            print(f"   [{self.name}] ESCALATION DETECTED")
            return {
                "response": "This issue requires immediate attention from our billing team.",
                "escalation": True,
                "priority": "high",
                "reason": "Billing dispute or urgent request"
            }
        
        # Detect request type
        if "upgrade" in query.lower():
            print(f"   [{self.name}] Identified: Account upgrade request")
            return {
                "response": "I can help you upgrade your account.",
                "action": "upgrade_account",
                "escalation": False
            }
        
        elif "help" in query.lower() or "support" in query.lower():
            print(f"   [{self.name}] Identified: General support request")
            return {
                "response": "I'm here to help with your request.",
                "action": "provide_support",
                "escalation": False
            }
        
        else:
            return {
                "response": "I'll assist you with your query.",
                "action": "general_assistance",
                "escalation": False
            }


class RouterAgent:
    """Orchestrator agent that coordinates specialist agents.
    
    Responsibilities:
    - Receive customer queries
    - Analyze query intent
    - Route to appropriate specialist agent
    - Coordinate responses from multiple agents
    """
    
    def __init__(self, db_path: str = "support.db"):
        """Initialize Router Agent with specialist agents.
        
        Args:
            db_path: Path to database
        """
        self.name = "Router Agent"
        self.customer_data_agent = CustomerDataAgent(db_path)
        self.support_agent = SupportAgent()
    
    def route_query(self, query: str) -> Dict[str, Any]:
        """Route query to appropriate agents and coordinate response.
        
        Args:
            query: Customer query
            
        Returns:
            Coordinated response from agents
        """
        print(f"\n{'='*70}")
        print(f" [{self.name}] Received query: {query}")
        print(f"{'='*70}")
        
        # Extract customer ID if present
        customer_id = self._extract_customer_id(query)
        
        response = {
            "query": query,
            "customer_data": None,
            "support_response": None,
            "coordination": []
        }
        
        # Step 1: Get customer data if needed
        if customer_id or "customer" in query.lower() or "list" in query.lower():
            print(f"\n A2A: [{self.name}] → [Customer Data Agent]")
            response["coordination"].append("Router → Customer Data Agent")
            
            context = {"customer_id": customer_id} if customer_id else {"status": "active"}
            
            if "open tickets" in query.lower():
                # Complex query: need to check each customer
                customers = self.customer_data_agent.mcp.list_customers(status="active")
                print(f"   [{self.name}] Found {len(customers)} active customers")
                print(f"   [{self.name}] Checking each for open tickets...")
                
                customers_with_tickets = []
                for customer in customers:
                    history = self.customer_data_agent.mcp.get_customer_history(customer['id'])
                    open_tickets = [t for t in history if t['status'] == 'open']
                    if open_tickets:
                        customer['open_tickets'] = open_tickets
                        customers_with_tickets.append(customer)
                
                response["customer_data"] = {"customers_with_open_tickets": customers_with_tickets}
                print(f"Found {len(customers_with_tickets)} customers with open tickets")
            else:
                customer_data = self.customer_data_agent.handle_query(query, context)
                response["customer_data"] = customer_data
        
        # Step 2: Route to support if needed
        if any(keyword in query.lower() for keyword in ['help', 'upgrade', 'charged', 'refund', 'support']):
            print(f"\n A2A: [{self.name}] → [Support Agent]")
            response["coordination"].append("Router → Support Agent")
            
            support_response = self.support_agent.handle_query(query, response["customer_data"])
            response["support_response"] = support_response
        
        # Step 3: Synthesize final response
        print(f"\n [{self.name}] Synthesizing final response...")
        response["final_message"] = self._synthesize_response(response)
        
        return response
    
    def _extract_customer_id(self, query: str) -> int:
        """Extract customer ID from query string.
        
        Args:
            query: Query string
            
        Returns:
            Customer ID or None
        """
        import re
        # Look for patterns like "ID 5", "customer 12345", etc.
        patterns = [
            r'ID\s+(\d+)',
            r'id\s+(\d+)',
            r'customer\s+(\d+)',
            r'\b(\d{4,5})\b'  # 4-5 digit numbers
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _synthesize_response(self, response_data: Dict[str, Any]) -> str:
        """Synthesize final response from agent data.
        
        Args:
            response_data: Data from specialist agents
            
        Returns:
            Final synthesized message
        """
        parts = []
        
        # Add customer data
        if response_data.get("customer_data"):
            data = response_data["customer_data"]
            if "customer" in data:
                customer = data["customer"]
                if "error" not in customer:
                    parts.append(f"Customer: {customer.get('name')} ({customer.get('email')})")
            
            if "customers_with_open_tickets" in data:
                count = len(data["customers_with_open_tickets"])
                parts.append(f"Found {count} active customers with open tickets")
        
        # Add support response
        if response_data.get("support_response"):
            support = response_data["support_response"]
            parts.append(support.get("response", ""))
            if support.get("escalation"):
                parts.append(f"  ESCALATION: {support.get('reason')}")
        
        return " | ".join(parts) if parts else "Query processed successfully"


def main():
    """Test agent coordination."""
    
    router = RouterAgent()
    
    # Test queries
    test_queries = [
        "Get customer information for ID 5",
        "I'm customer 12345 and need help upgrading my account",
        "Show me all active customers who have open tickets",
        "I've been charged twice, please refund immediately!",
    ]
    
    for query in test_queries:
        result = router.route_query(query)
        print(f"\n Final Response: {result['final_message']}\n")
        print("="*70 + "\n")


if __name__ == "__main__":
    main()
