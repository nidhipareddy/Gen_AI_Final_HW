# Multi-Agent Customer Service System with A2A and MCP

A multi-agent customer service system where specialized agents coordinate using Agent-to-Agent (A2A) communication and access customer data through the Model Context Protocol (MCP).

## 📋 Assignment Overview

This project implements a three-agent system:
- **Router Agent** (Orchestrator): Coordinates queries and routes to specialists
- **Customer Data Agent** (Specialist): Accesses database via MCP tools
- **Support Agent** (Specialist): Handles customer support with escalation

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Router Agent                           │
│                    (Orchestrator)                           │
│  - Receives customer queries                                │
│  - Analyzes intent                                          │
│  - Coordinates specialist agents                            │
└────────────┬─────────────────────────┬──────────────────────┘
             │                         │
             │ A2A                     │ A2A
             ↓                         ↓
   ┌─────────────────┐      ┌──────────────────┐
   │ Customer Data   │      │ Support Agent    │
   │ Agent           │      │                  │
   │ - MCP Tools     │      │ - Support logic  │
   │ - Database ops  │      │ - Escalation     │
   └────────┬────────┘      └──────────────────┘
            │
            │ MCP
            ↓
   ┌────────────────┐
   │ SQLite         │
   │ Database       │
   │ - Customers    │
   │ - Tickets      │
   └────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd multi-agent-customer-service
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up the database**
```bash
python database_setup.py
```

This creates:
- `support.db` SQLite database
- Customers table (15 sample customers + customer 12345)
- Tickets table (25 sample tickets)
- Proper indexes and triggers

## Project Structure

```
multi-agent-customer-service/
├── database_setup.py          # Database schema and sample data (Part 2)
├── mcp_tools.py               # 5 MCP tools implementation (Part 2)
├── agents.py                  # Three agent implementations (Part 1 & 3)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── Complete_Part1_Part2_Part3_FINAL.ipynb  # Full Colab demonstration
```

## Implementation Details

### Part 1: System Architecture

**Three Specialized Agents:**

1. **Router Agent (Orchestrator)**
   - Receives customer queries
   - Analyzes query intent
   - Routes to appropriate specialist
   - Coordinates multi-agent responses

2. **Customer Data Agent (Specialist)**
   - Accesses customer database via MCP
   - Retrieves customer information
   - Updates customer records
   - Handles data validation

3. **Support Agent (Specialist)**
   - Handles customer support queries
   - Detects escalation triggers
   - Requests customer context
   - Provides solutions/recommendations

### Part 2: MCP Integration

**5 Required MCP Tools:**

```python
# Tool 1: Get customer by ID
get_customer(customer_id: int) -> Dict
# Uses: customers.id

# Tool 2: List customers with filter
list_customers(status: str, limit: int) -> List[Dict]
# Uses: customers.status

# Tool 3: Update customer data
update_customer(customer_id: int, data: Dict) -> Dict
# Uses: customers fields (name, email, phone, status)

# Tool 4: Create support ticket
create_ticket(customer_id: int, issue: str, priority: str) -> Dict
# Uses: tickets fields

# Tool 5: Get customer ticket history
get_customer_history(customer_id: int) -> List[Dict]
# Uses: tickets.customer_id
```

**Database Schema:**

Customers Table:
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL)
- email (TEXT)
- phone (TEXT)
- status (TEXT: 'active' or 'disabled')
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

Tickets Table:
- id (INTEGER PRIMARY KEY)
- customer_id (INTEGER FK → customers.id)
- issue (TEXT NOT NULL)
- status (TEXT: 'open', 'in_progress', 'resolved')
- priority (TEXT: 'low', 'medium', 'high')
- created_at (DATETIME)

### Part 3: A2A Coordination

**Implementation Approach:** Lab Notebook Pattern (Option A)

The system demonstrates explicit A2A coordination with logging:

```python
Router Agent receives query
    ↓
 A2A: Router → Customer Data Agent
    Customer Data Agent calls MCP tools
    ✓ Returns customer data
    ↓
 A2A: Router → Support Agent
    Support Agent analyzes with customer context
    ✓ Returns support response (+ escalation if needed)
    ↓
 Router synthesizes final response
    ↓
 Returns coordinated result to user
```

##  Running Tests

### Test All Components Separately

1. **Test Database Setup:**
```bash
python database_setup.py
```

2. **Test MCP Tools:**
```bash
python mcp_tools.py
```
Tests all 5 MCP tools with sample queries.

3. **Test Agent Coordination:**
```bash
python agents.py
```
Demonstrates A2A coordination with test queries.

### Full End-to-End Test

The Colab notebook `Complete_Part1_Part2_Part3_FINAL.ipynb` provides complete demonstration with all 5 test scenarios.