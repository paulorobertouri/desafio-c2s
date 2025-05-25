from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Command to run the server
    args=["server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()

            # Get a prompt
            prompt = await session.get_prompt(
                "prompt",  # Name of the prompt
                arguments={"name": "World"},  # Arguments for the prompt
            )

            # Get a resource
            resource = await session.read_resource(
                "hello://Alice"  # Resource URL
            )

            # Call a tool
            tool = await session.call_tool(
                "add",  # Name of the tool
                arguments={"a": 5, "b": 3}  # Arguments for the tool
            )

            # Print results
            print("Tool Result:", tool.content[0].text)
            print("Resource Result:", resource.contents[0].text)
            print("Prompt Result:", prompt.messages[0].content.text)

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
