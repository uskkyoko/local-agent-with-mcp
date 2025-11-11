from mcp.server.fastmcp import FastMCP
from typing import Union
import uvicorn

mcp = FastMCP("calculator")

@mcp.tool()
def add(a:int, b: int) -> int:
    """Adds two integers together"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtracts the second integer from the first."""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiplies two integers together."""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> Union[float, str]:
    """
    Divides the first integer by the second.
    Returns a float or an error message if dividing by zero.
    """
    if b == 0:
        return "Error: Cannot divide by zero."
    return a / b

def main():
    """Entry point for the direct execution server."""
    mcp.run()

if __name__ == "__main__":

    main()