"""
Client for interacting with the Virtual Car Agent server.
"""
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import logging

PROMPT_INTRO = "\nWelcome to the Virtual Car Agent!"
PROMPT_EXAMPLES = """
I can help you find a car that matches your preferences.\n
You can tell me what you're looking for in a car. For example:
- I want a Toyota from 2018 or newer, automatic, up to $50,000.
- Show me a red Honda with less than 50,000 km.
- Any electric car below $100,000.\n"""
PROMPT_ASK = "What kind of car are you looking for? "

server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
    env=None,
)


async def run():
    """
    Run the client interaction loop.
    """
    print(PROMPT_INTRO)
    print(PROMPT_EXAMPLES)
    user_query = input(PROMPT_ASK).strip()
    if not user_query:
        print("Please enter a valid car search query.")
        return
    print("\nAnalyzing your request...\n")
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("Searching for cars that match your preferences...\n")
                resource = await session.call_tool(
                    "search_cars",
                    arguments={"user_query": user_query}
                )
                print("Results:\n")
                print(resource.content[0].text)
    except Exception as e:
        logging.error(f"Error connecting to server: {e}")
        print(f"Error connecting to server: {e}")


if __name__ == "__main__":
    asyncio.run(run())
