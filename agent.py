import json
from typing import List, Union

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from fastmcp import Client 
import asyncio

try:
    calculator_client = Client("server_calculator.py")
    calculator_client.list_tools()
    print("✅ Connected to FastMCP 'calculator' server.")
    notes_client = Client("server_notes.py")
    notes_client.list_tools()
    print("✅ Connected to FastMCP 'notes' server.")
except Exception as e:
    print(f"❌ Failed to connect to FastMCP server. Is it running?")
    print(f"Error: {e}")
    exit()

@tool
def add(a: int, b: int) -> int:
    """Adds two integers together"""
    print(f"--- Calling MCP Tool: add({a}, {b}) ---")
    
    async def _call_mcp():
        async with calculator_client:
            return await calculator_client.call_tool("add", {"a": a, "b": b})
    return asyncio.run(_call_mcp())


@tool
def subtract(a: int, b: int) -> int:
    """Subtracts the second integer from the first."""
    print(f"--- Calling MCP Tool: subtract({a}, {b}) ---")
    
    async def _call_mcp():
        async with calculator_client:
            return await calculator_client.call_tool("subtract", {"a": a, "b": b})
    return asyncio.run(_call_mcp())


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers together."""
    print(f"--- Calling MCP Tool: multiply({a}, {b}) ---")
    
    async def _call_mcp():
        async with calculator_client:
            return await calculator_client.call_tool("multiply", {"a": a, "b": b})
    return asyncio.run(_call_mcp())

@tool
def divide(a: int, b: int) -> Union[float, str]:
    """
    Divides the first integer by the second.
    Returns a float or an error message if dividing by zero.
    """
    print(f"--- Calling MCP Tool: divide({a}, {b}) ---")
    
    async def _call_mcp():
        async with calculator_client:
            return await calculator_client.call_tool("divide", {"a": a, "b": b})
    return asyncio.run(_call_mcp())

@tool
def add_note(message: str) -> str:
    """Adds a note to the notes server."""
    print(f"--- Calling MCP Tool: add_note('{message}') ---")
    
    async def _call_mcp():
        async with notes_client:
            return await notes_client.call_tool("add_note", {"message": message})
    return asyncio.run(_call_mcp())

@tool
def read_notes() -> str:
    """Retrieves all notes from the notes server."""
    print(f"--- Calling MCP Tool: read_notes() ---")
    
    async def _call_mcp():
        async with notes_client:
            return await notes_client.call_tool("read_notes")
    return asyncio.run(_call_mcp())


tools = [add, subtract, multiply, divide, add_note, read_notes]
model = ChatOllama(model="llama3.1:8b")

system_prompt = """You are DevHelper, an expert software development assistant.
    Your job is to read, review, explain, and improve code.
    You can help with debugging, refactoring, architecture decisions, and explaining difficult concepts.

    You also have access to a calculator with the following tools:
    - add
    - subtract
    - multiply
    - divide
    If the user asks a math question, use these tools.

    Also, you can manage sticky notes with these tools:
    - add_note
    - read_notes
    If the user wants to save or read notes, use these tools.

    For all other requests, use your software development knowledge.
    """

agent = create_agent(model, tools, system_prompt=system_prompt)


def run_agent(user_input: str) -> AIMessage:
    try:
        input_data = {
            "messages": [HumanMessage(content=user_input)]
        }
        
        response = agent.invoke(
            input_data,
            config={"recursion_limit": 50}
        )

        final_content = response["messages"][-1].content
        return AIMessage(content=str(final_content))

    except Exception as e:
        print(f"\n[Agent Error]: {e}") 
        return AIMessage(content=f"Error: {str(e)}. Try phrasing it differently.")


if __name__ == "__main__":
    print("=" * 60)
    print("DevHelper Agent (with Calculator & Notes Tools)")
    print("=" * 60)
    print("... (Startup messages) ...")
    print("=" * 60)

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        print("Agent: ", end="", flush=True)
        response = run_agent(user_input)
        
        print(response.content) 
        print()