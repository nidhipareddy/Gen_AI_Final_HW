# Multi-Agent Customer Service System with A2A and MCP

A multi-agent customer service system where specialized agents coordinate using Agent-to-Agent (A2A) communication and access customer data through the Model Context Protocol (MCP).

## 🎯 System Overview

This system implements three specialized agents that work together to handle customer service queries:

1. **Router Agent** - Orchestrator that analyzes queries and coordinates specialist agents
2. **Customer Data Agent** - Specialist that accesses customer database via MCP
3. **Support Agent** - Specialist that handles support queries and provides solutions

## 🏗️ Architecture

```
User Query
    ↓
Router Agent (SequentialAgent)
    ↓
    ├→ Customer Data Agent (A2A port 10030)
    │      ↓
    │  MCPToolset → HTTP → MCP Server (Flask port 5000)
    │                           ↓
    │                      SQLite Database
    │
    └→ Support Agent (A2A port 10031)
           ↓
       Final Response
```

### Key Components

- **MCP Server**: Flask application providing 5 tools via HTTP JSON-RPC protocol
- **A2A Coordination**: Agents communicate via RemoteA2aAgent references
- **MCPToolset**: Google ADK component connecting agents to MCP Server

## 📋 Requirements

```
Python 3.10+
google-adk==1.9.0
a2a-sdk
flask
flask-cors
sqlite3
uvicorn
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd multi-agent-customer-service
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Database

```bash
python database_setup.py
```

This creates `support.db` with sample customer and ticket data.

### 4. Run the System

#### Option A: Colab Notebook (Recommended)

1. Upload `Complete_Part1_Part2_Part3_FINAL.ipynb` to Google Colab
2. Run all cells sequentially
3. The notebook will:
   - Install dependencies
   - Set up database
   - Start MCP Server (port 5000)
   - Create and start agents (ports 10030, 10031)
   - Run test scenarios

#### Option B: Python Script

```bash
python run_system.py
```

## 🧪 Test Scenarios

The system handles these test queries:

### 1. Simple Query
```
Query: "Get customer information for ID 5"
Flow: Router → Customer Data Agent → MCP Server → Database
```

### 2. Coordinated Query
```
Query: "I'm customer 5 and need help upgrading my account"
Flow: Router → Customer Data Agent (fetch data) → Support Agent (generate response)
```

### 3. Complex Query
```
Query: "Show me all active customers who have open tickets"
Flow: Router → Customer Data Agent (list) → Support Agent (filter tickets)
```

### 4. Escalation
```
Query: "I've been charged twice, please refund immediately!"
Flow: Router detects urgency → Prioritizes → Support Agent with high priority
```

### 5. Multi-Intent
```
Query: "Update my email to new@email.com and show my ticket history"
Flow: Router → Customer Data Agent (update + history) → Support Agent (format)
```

## 🔧 MCP Tools

The MCP Server provides 5 tools:

### 1. get_customer
```python
Parameters:
  - customer_id (int): Customer ID to retrieve

Returns: Customer details (name, email, phone, status)
```

### 2. list_customers
```python
Parameters:
  - status (str): Filter by status ('active' or 'disabled')
  - limit (int): Maximum number of results

Returns: List of customers
```

### 3. update_customer
```python
Parameters:
  - customer_id (int): Customer ID to update
  - data (dict): Fields to update (name, email, phone, status)

Returns: Success status
```

### 4. create_ticket
```python
Parameters:
  - customer_id (int): Customer ID
  - issue (str): Ticket description
  - priority (str): 'low', 'medium', or 'high'

Returns: New ticket ID
```

### 5. get_customer_history
```python
Parameters:
  - customer_id (int): Customer ID

Returns: List of all tickets for customer
```

## 📁 Project Structure

```
multi-agent-customer-service/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── database_setup.py                   # Database initialization
├── mcp_server.py                       # MCP Server
├── agents.py                           # Agent definitions
├── run_system.py                       # Run full system
├── CORRECTED_complete_notebook.ipynb  # Colab notebook
└── support.db                          # SQLite database (generated)
```

