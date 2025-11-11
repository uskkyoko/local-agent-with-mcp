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

Reflection:
I was assigned with calculator and data analysis MCP, but I haven't found any data analysis MCPs that would be easily integrated into my local agent, mostly because of my os. So I have included self-written calculator MCP server and found the AI notes MCP server, all of which are made using FastMCP. I have used FastMCP Client, because it is an easy way to connect your local AI agent using Python. The biggest hurdle was to connect my local agent to the MCP servers. I have tried using connections via https, ollama-mcp-bridge, but none worked for me. Now my local model can easily access calculator tools and create notes file directly in my project folder, as well as reading all my notes. If I have continued this project, I would definetely write an data analysis MCP server and use some already existing GitHub MCPs, so the developer helper would be much more efficient.
