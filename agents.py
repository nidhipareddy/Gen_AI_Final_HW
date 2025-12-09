"""
Agent Implementations for Multi-Agent Customer Service System
Includes Router, Customer Data, and Support agents with A2A coordination
"""

from google.adk.agents import Agent, SequentialAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
from a2a.types import AgentCard, AgentCapabilities, AgentSkill, TransportProtocol


# ============================================================================
# CUSTOMER DATA AGENT
# ============================================================================

def create_customer_data_agent():
    """
    Create Customer Data Agent with MCP tools
    
    This agent:
    - Accesses customer database via MCP Server
    - Has 5 MCP tools available via MCPToolset
    - Executes tools directly when asked
    """
    agent = Agent(
        model='gemini-2.0-flash-exp',
        name='customer_data_agent',
        instruction="""
        You are a Customer Data Agent with access to customer database via MCP tools.
        
        Available MCP tools:
        1. get_customer(customer_id: int) - Get customer by ID
        2. list_customers(status: str, limit: int) - List customers by status
        3. update_customer(customer_id: int, data: dict) - Update customer info
        4. create_ticket(customer_id: int, issue: str, priority: str) - Create ticket
        5. get_customer_history(customer_id: int) - Get customer's tickets
        
        When asked about customer data:
        - Identify the appropriate tool
        - Execute it immediately
        - Return clear results
        
        Always use tools - don't make up data!
        """,
        tools=[
            MCPToolset(
                connection_params=StreamableHTTPConnectionParams(
                    url="http://localhost:5000/mcp"
                )
            )
        ]
    )
    
    return agent


def create_customer_data_agent_card():
    """Create Agent Card for Customer Data Agent"""
    return AgentCard(
        name='Customer Data Agent',
        url='http://localhost:10030',
        description='Accesses customer database via MCP for data operations',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='customer_data_operations',
                name='Customer Data Operations',
                description='Retrieve, update, and manage customer information',
                tags=['customer', 'data', 'mcp'],
                examples=[
                    'Get customer by ID',
                    'List active customers',
                    'Update customer email'
                ]
            )
        ]
    )


# ============================================================================
# SUPPORT AGENT
# ============================================================================

def create_support_agent():
    """
    Create Support Agent for customer service
    
    This agent:
    - Handles general customer support queries
    - Detects escalations and urgency
    - Provides helpful responses
    """
    agent = Agent(
        model='gemini-2.0-flash-exp',
        name='support_agent',
        instruction="""
        You are a Support Agent handling customer service queries.

        Responsibilities:
        - Handle general customer support questions
        - Provide solutions and recommendations
        - Identify when issues need escalation
        - Request customer context when needed

        Escalation triggers:
        - Billing disputes
        - Urgent requests
        - Refund requests
        - Account security issues

        Priority detection:
        - HIGH: Billing, refunds, security, data loss
        - MEDIUM: Feature requests, functionality issues
        - LOW: Minor bugs, general questions

        Always maintain a helpful and professional tone.
        """,
        tools=[]  # Support agent doesn't need MCP tools directly
    )
    
    return agent


def create_support_agent_card():
    """Create Agent Card for Support Agent"""
    return AgentCard(
        name='Support Agent',
        url='http://localhost:10031',
        description='Handles customer support queries and provides solutions',
        version='1.0',
        capabilities=AgentCapabilities(streaming=True),
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        preferred_transport=TransportProtocol.jsonrpc,
        skills=[
            AgentSkill(
                id='customer_support',
                name='Customer Support',
                description='Provide support and detect escalations',
                tags=['support', 'escalation'],
                examples=[
                    'Help with account upgrade',
                    'Handle billing issues',
                    'Detect urgent requests'
                ]
            )
        ]
    )


# ============================================================================
# REMOTE AGENT REFERENCES (A2A)
# ============================================================================

def create_remote_customer_data_agent():
    """Create remote reference to Customer Data Agent for A2A"""
    return RemoteA2aAgent(
        name='customer_data',
        description='Customer database operations via MCP',
        agent_card='http://localhost:10030/.well-known/a2a-agent-card.json'
    )


def create_remote_support_agent():
    """Create remote reference to Support Agent for A2A"""
    return RemoteA2aAgent(
        name='support',
        description='Customer support and solutions',
        agent_card='http://localhost:10031/.well-known/a2a-agent-card.json'
    )


# ============================================================================
# ROUTER AGENT
# ============================================================================

def create_router_agent(remote_customer_data, remote_support):
    """
    Create Router Agent using SequentialAgent
    
    This agent:
    - Receives customer queries
    - Analyzes intent
    - Coordinates specialist agents via A2A
    - Synthesizes final response
    
    Args:
        remote_customer_data: RemoteA2aAgent reference to Customer Data Agent
        remote_support: RemoteA2aAgent reference to Support Agent
    """
    router = SequentialAgent(
        name='router_agent',
        sub_agents=[remote_customer_data, remote_support]
    )
    
    return router


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_agent_info(agent, agent_name):
    """Print agent configuration details"""
    print(f"\n✅ {agent_name} created")
    print(f"   Model: {agent.model}")
    print(f"   Name: {agent.name}")
    if hasattr(agent, 'tools') and agent.tools:
        print(f"   Tools: {len(agent.tools)} tool(s) available")
    else:
        print(f"   Tools: None (uses coordination)")


def print_router_info(router):
    """Print router configuration details"""
    print(f"\n✅ Router Agent created")
    print(f"   Name: {router.name}")
    print(f"   Type: SequentialAgent (orchestrator)")
    print(f"   Sub-agents: {len(router.sub_agents)}")
    for agent in router.sub_agents:
        print(f"   - {agent.name}")


# ============================================================================
# MAIN SETUP FUNCTION
# ============================================================================

def setup_agents():
    """
    Setup all agents and return them
    
    Returns:
        tuple: (customer_data_agent, support_agent, router_agent, agent_cards)
    """
    print("="*70)
    print("SETTING UP AGENTS")
    print("="*70)
    
    # Create agents
    customer_data_agent = create_customer_data_agent()
    support_agent = create_support_agent()
    
    # Create agent cards
    customer_data_card = create_customer_data_agent_card()
    support_agent_card = create_support_agent_card()
    
    # Create remote references
    remote_customer_data = create_remote_customer_data_agent()
    remote_support = create_remote_support_agent()
    
    # Create router
    router_agent = create_router_agent(remote_customer_data, remote_support)
    
    # Print info
    print_agent_info(customer_data_agent, "Customer Data Agent")
    print_agent_info(support_agent, "Support Agent")
    print_router_info(router_agent)
    
    print("\n" + "="*70)
    print("✅ ALL AGENTS CREATED")
    print("="*70)
    
    return (
        customer_data_agent,
        support_agent,
        router_agent,
        customer_data_card,
        support_agent_card
    )


if __name__ == "__main__":
    # Test agent creation
    setup_agents()
    print("\n✅ Agent setup test complete!")
