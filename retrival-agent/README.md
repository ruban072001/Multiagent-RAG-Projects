# **AgenticCrew: Intelligent Document Retrieval and Response System**  

**AgenticCrew** is a modular and extensible framework designed for intelligent document retrieval and response generation. Built using the CrewAI library, it efficiently processes user queries, retrieves relevant content from documents, ranks it, and generates accurate responses.  

This system is self-contained, relying exclusively on a **custom document processing tool** for content retrieval and ranking.  

---

## **Features**  

### **Agent-Based Architecture**  
AgenticCrew employs a robust three-agent system to streamline document processing and response generation:  

- **Agent 1: Query Parser and Retriever**  
  - Analyzes user queries to extract key terms or topics for effective processing and Searches the document database to locate and retrieve relevant files and content.  

- **Agent 2: Document Ranker**  
  - Rank the documents based on similarity to user query

- **Agent 3: Response Generator**  
  - Synthesizes concise and accurate responses from the top-ranked documents.  

### **Custom Tool Integration**  
- **Document Processing Tool:** Handles all document search, ranking, and retrieval tasks to ensure a self-contained and efficient workflow.  

### **Flexible Workflow**  
- AgenticCrew supports both sequential and hierarchical processing pipelines, making it adaptable to complex query-processing scenarios.  

### **Configurable Design**  
- Easily configure agents and tasks using the `agents.yaml` and `tasks.yaml` files located in the `config` directory.  

---

## **Setup Instructions**  

Follow these steps to set up and run AgenticCrew:  

### **1. Clone the Repository**  
```bash
git clone https://github.com/ruban072001/Multiagent-RAG-Projects.git
