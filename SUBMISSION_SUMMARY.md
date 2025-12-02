# Assignment Submission Summary
## Multi-Agent Customer Service System with A2A and MCP

**Student Name:** Nidhi Pareddy
**Date:** December 1, 2025
**Course:** Multi-Agent Systems

---

## Deliverables Checklist

### 1. Code Repository (GitHub)

**Repository Contents:**
- `database_setup.py` - Database schema and sample data (Part 2)
- `mcp_tools.py` - 5 MCP tools implementation (Part 2)
- `agents.py` - Three agent implementations (Part 1 & 3)
- `setup.py` - Automated setup and verification script
- `requirements.txt` - Python dependencies clearly listed
- `README.md` - Comprehensive setup and usage instructions

### 2. Colab Notebook

**File:** `Complete_Part1_Part2_Part3_FINAL.ipynb`

**Contents:**
- end-to-end demonstration
- All 5 test scenarios with output
- Part 1: Three agents (Router, Customer Data, Support)
- Part 2: 5 MCP tools with database
- Part 3: A2A coordination with explicit logging

### 3. Conclusion

Located in: README.md (sections "What I Learned" and "Challenges Faced")
Also included at end of Colab notebook.

---

## 🏗️ Implementation Summary

### Part 1: System Architecture (3 Agents)

**1. Router Agent (Orchestrator)**
- File: `agents.py` - `RouterAgent` class
- Responsibilities:
  - Receives customer queries
  - Analyzes query intent using regex patterns
  - Routes to appropriate specialist agents
  - Coordinates multi-agent responses
  - Synthesizes final responses
- Implementation: Coordinates `CustomerDataAgent` and `SupportAgent`

**2. Customer Data Agent (Specialist)**
- File: `agents.py` - `CustomerDataAgent` class
- Responsibilities:
  - Accesses customer database via MCP tools
  - Retrieves customer information
  - Updates customer records
  - Validates data operations
- Integration: Uses `MCPTools` class for all database operations

**3. Support Agent (Specialist)**
- File: `agents.py` - `SupportAgent` class
- Responsibilities:
  - Handles general customer support queries
  - Detects escalation triggers (billing, urgent keywords)
  - Requests customer context from Data Agent
  - Provides solutions and recommendations
- Features: Automatic escalation detection and priority flagging

### Part 2: MCP Integration (5 Tools)

**Database:** SQLite (`support.db`)

**Schema:**
- `customers` table: id, name, email, phone, status, created_at, updated_at
- `tickets` table: id, customer_id, issue, status, priority, created_at
- Indexes on: email, customer_id, status
- Trigger for automatic `updated_at` timestamp

**MCP Tools** (File: `mcp_tools.py` - `MCPTools` class):

1. **get_customer(customer_id)** - Uses `customers.id`
   - Returns single customer record
   - Handles not found cases

2. **list_customers(status, limit)** - Uses `customers.status`
   - Returns filtered customer list
   - Supports pagination with limit

3. **update_customer(customer_id, data)** - Uses `customers` fields
   - Updates name, email, phone, or status
   - Validates fields and returns updated fields list

4. **create_ticket(customer_id, issue, priority)** - Uses `tickets` fields
   - Creates new support ticket
   - Validates priority levels
   - Returns ticket ID and details

5. **get_customer_history(customer_id)** - Uses `tickets.customer_id`
   - Returns all tickets for a customer
   - Ordered by created_at DESC

**Sample Data:**
- 15 diverse customers (John Doe, Jane Smith, Charlie Brown, etc.)
- 25 tickets (various statuses and priorities)
- Customer 12345 added for test scenarios

### Part 3: A2A Coordination

**Approach:** Option A - Lab Notebook Pattern

**Implementation:**
- Router Agent orchestrates all coordination
- Explicit logging of agent-to-agent communication
- Format: `A2A: [Router Agent] → [Customer Data Agent]`
- Each agent logs its actions: `[Agent Name] Action performed`
- Clear flow: Query → Route → Execute → Synthesize → Respond

**5 Test Scenarios Demonstrated:**

1. **Simple Query**: "Get customer information for ID 5"
   - Single agent path
   - Direct MCP tool call
   - Output: Customer data for Charlie Brown

2. **Coordinated Query**: "I'm customer 12345 and need help upgrading"
   - Multi-agent coordination
   - Data Agent → Support Agent → Router synthesis
   - Output: Customer context + upgrade assistance

3. **Complex Query**: "Show all active customers who have open tickets"
   - Multi-step coordination
   - List customers → Check each for open tickets → Filter results
   - Output: Customers with their open ticket details

4. **Escalation**: "I've been charged twice, refund immediately!"
   - Escalation detection by Support Agent
   - Priority flagging
   - Output: Escalation notice with high priority

5. **Multi-Intent**: "Update email and show ticket history"
   - Parallel task execution
   - Update operation + history retrieval
   - Output: Update confirmation + ticket list

---

## Testing & Verification

### How to Verify the Implementation

1. **Setup the project:**
   ```bash
   python setup.py
   ```

2. **Test MCP tools individually:**
   ```bash
   python mcp_tools.py
   ```
   Expected: All 5 tools execute successfully with sample data

3. **Test agent coordination:**
   ```bash
   python agents.py
   ```
   Expected: 4 test queries with A2A logging and responses

4. **Run full Colab notebook:**
   - Open `Complete_Part1_Part2_Part3_FINAL.ipynb` in Colab
   - Run all cells
   - Expected: All 5 scenarios execute with proper output

### Test Results Summary

All test scenarios pass with proper A2A coordination logging:
- Scenario 1: Simple query - Single agent MCP call
- Scenario 2: Coordinated query - Multi-agent cooperation
- Scenario 3: Complex query - Multi-step with filtering
- Scenario 4: Escalation - Priority detection and flagging
- Scenario 5: Multi-intent - Parallel task execution

---

## Learning Outcomes

### What I Learned 

Through this assignment, I gained hands-on experience implementing a multi-agent system with A2A coordination and MCP integration. The key learning was understanding how to properly integrate all three parts: the agents from Part 1 must use the MCP tools from Part 2, coordinated through Part 3's orchestration patterns. I learned that the Router Agent acts as an intelligent orchestrator, analyzing queries using pattern matching and routing them to specialized agents with clear separation of concerns. The MCP tools provide a clean interface between agent logic and data access, making the system modular and maintainable. I also learned about A2A communication patterns and how proper logging makes multi-agent interactions transparent and debuggable.

### Challenges Faced 

The main challenge was adapting the reference notebook's A2A server pattern (which uses separate HTTP servers on different ports) to work in a Colab environment where persistent servers are difficult to maintain. I solved this by implementing the same logical coordination flow with direct function calls while preserving explicit A2A communication logging at each step. Another challenge was demonstrating clear A2A coordination for complex queries like "show all active customers with open tickets," which required the Customer Data Agent to make multiple MCP calls (list customers, then get history for each) and filter results before returning to the Router. Finally, balancing code simplicity for educational purposes while maintaining production-quality patterns like error handling, type hints, and comprehensive logging required careful design decisions.

---

## How to Run

### Google Colab (Recommended)
1. Open `Complete_Part1_Part2_Part3_FINAL.ipynb` in Colab
2. Add GOOGLE_API_KEY to Colab secrets (if using Gemini features)
3. Run all cells
4. See all 5 test scenarios with output