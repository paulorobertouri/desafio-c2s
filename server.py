# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Server")


# Add a tool that sums two integers
@mcp.tool(None, description="Sum two integers")
def add(a: int, b: int) -> int:
    return a + b


# Add a resource that returns a greeting
@mcp.resource("hello://{name}", description="Greeting resource")
def get_greeting(name: str) -> str:
    return f"Hello, {name}!"


# Add a prompt that takes a string argument and returns a greeting
@mcp.prompt("prompt", description="Greeting prompt")
def greeting_prompt(name: str) -> str:
    return f"Hello, {name} from the prompt!"


if __name__ == "__main__":
    mcp.run()
