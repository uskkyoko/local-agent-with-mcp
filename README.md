LangChain Agent with External Tools via FastMCP
This project demonstrates a DevHelper conversational AI agent built with LangChain and a local Ollama model (llama3.1:8b).

The unique feature of this project is its architecture: all tools (like a calculator and a note-taking service) run in separate, independent processes. The main LangChain agent communicates with these tools using the fastmcp (Fast Microservice Communication Protocol) library, treating them as microservices.

🏛️ Architecture
This project is not a single-file script. It runs in at least three separate processes:

The Main Agent (agent.py):

This is the "brain" of the operation.

It runs the LangChain agent and the Ollama LLM.

It defines LangChain @tool functions that act as clients.

When the LLM decides to use a tool, this client script sends a request to the appropriate MCP server.

The MCP Servers (server_calculator.py, server_notes.py):

These are the "hands" of the operation.

Each server is a lightweight, standalone Python process.

They define the actual tool logic (e.g., def add(...)) using the @mcp.tool() decorator.

They listen for requests from the agent's client, run the function, and return the result.

This decoupled architecture is powerful because it allows you to:

Run tools in different environments (e.g., a Docker container).

Use different Python versions or dependencies for each tool.

Update a tool by simply restarting its server, without touching the main agent.

✨ Features
Conversational AI: Uses a local llama3.1:8b model via langchain-ollama to understand requests.

Calculator Tool: Can perform add, subtract, multiply, and divide operations.

Notes Tool: Can save notes to a persistent file (notes.txt).

Microservice Architecture: Tools are isolated in their own processes using FastMCP.