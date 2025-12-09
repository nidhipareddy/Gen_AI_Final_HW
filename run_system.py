"""
Run Complete Multi-Agent Customer Service System
Starts MCP Server, agents, and runs test scenarios
"""

import time
import threading
import sys
from mcp_server import MCPServer
from agents import setup_agents


def start_mcp_server_background():
    """Start MCP Server in background thread"""
    print("\n🚀 Starting MCP Server...")
    server = MCPServer(db_path='support.db', port=5000)
    server.run(debug=False)


def run_test_scenarios():
    """Run the 5 required test scenarios"""
    
    test_queries = [
        {
            'name': 'Scenario 1: Simple Query',
            'query': 'Get customer information for ID 5',
            'expected': 'Single agent, straightforward MCP call'
        },
        {
            'name': 'Scenario 2: Coordinated Query',
            'query': "I'm customer 5 and need help upgrading my account",
            'expected': 'Multiple agents coordinate: data fetch + support response'
        },
        {
            'name': 'Scenario 3: Complex Query',
            'query': 'Show me all active customers who have open tickets',
            'expected': 'Negotiation between data and support agents'
        },
        {
            'name': 'Scenario 4: Escalation',
            'query': "I've been charged twice, please refund immediately!",
            'expected': 'Router identifies urgency and routes appropriately'
        },
        {
            'name': 'Scenario 5: Multi-Intent',
            'query': 'Update my email to new@email.com and show my ticket history',
            'expected': 'Parallel task execution and coordination'
        }
    ]
    
    print("\n" + "="*80)
    print("RUNNING TEST SCENARIOS")
    print("="*80)
    
    for i, scenario in enumerate(test_queries, 1):
        print(f"\n{'='*80}")
        print(f"{scenario['name']}")
        print(f"{'='*80}")
        print(f"Query: {scenario['query']}")
        print(f"Expected: {scenario['expected']}")
        print(f"\nNote: In actual implementation, router_agent.run(scenario['query'])")
        print(f"      would execute and coordinate agents via A2A protocol")
        print(f"{'='*80}\n")


def main():
    """Main execution function"""
    print("="*80)
    print("MULTI-AGENT CUSTOMER SERVICE SYSTEM")
    print("="*80)
    
    # Check if database exists
    import os
    if not os.path.exists('support.db'):
        print("\n❌ Database not found!")
        print("Please run: python database_setup.py")
        sys.exit(1)
    
    print("\n✅ Database found")
    
    # Start MCP Server in background
    mcp_thread = threading.Thread(target=start_mcp_server_background, daemon=True)
    mcp_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    print("✅ MCP Server is running")
    
    # Setup agents
    print("\n" + "="*80)
    agents = setup_agents()
    
    # In a full implementation, you would:
    # 1. Start A2A servers for each agent
    # 2. Run test scenarios
    # 3. Capture and display results
    
    print("\n" + "="*80)
    print("SYSTEM READY")
    print("="*80)
    print("\nTo run this system:")
    print("1. Use the Colab notebook for full A2A server setup")
    print("2. Or implement A2A servers here using uvicorn")
    print("3. Then run test scenarios via router_agent.run(query)")
    
    # Run test scenarios (demonstration)
    run_test_scenarios()
    
    print("\n" + "="*80)
    print("Note: For full execution with A2A coordination,")
    print("please use the Colab notebook which includes:")
    print("  - A2A server startup for each agent")
    print("  - Full agent-to-agent communication")
    print("  - Complete test scenario execution")
    print("="*80)
    
    # Keep server running
    print("\n✅ MCP Server is running in background")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n✅ Shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
