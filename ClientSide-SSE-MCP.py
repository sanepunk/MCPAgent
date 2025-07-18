from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import asyncio
from groq import AsyncGroq
from contextlib import AsyncExitStack
import json
from typing import Any, Dict, Optional, List
from dotenv import load_dotenv
from datetime import timedelta
import os   
load_dotenv()

server_side_mcp_script = os.path.join(os.path.dirname(__file__), "ServerSideMCP.py")

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY_2")
# print(f"Using GROQ_API_KEY: {os.getenv('GROQ_API_KEY_1')}")

class MCPGroqClient:
    def __init__(self, model: str = "llama3-8b-8192"):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.GroqClient = AsyncGroq()
        self.model = model
        self.stdio: Optional[Any] = None
        self.write: Optional[Any] = None

    async def connect_to_server(self, script: str = server_side_mcp_script) -> None:
        """
        Connect to the MCP server using stdio.
        Args:
            script (str): The script to run the MCP server.
        """
        print(f"Connecting to MCP server using script: {script}")
        server_params = StdioServerParameters(
            command="python",
            args=[script]
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        self.stdio, self.write = stdio_transport

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(
                self.stdio,
                self.write
            )
        )

        await self.session.initialize()

        tools_result = await self.session.list_tools()
        print("\nConnected to MCP server with tools:")
        for tool in tools_result.tools:
            print(f"- {tool.name}")
        
    async def get_mcp_tools(self) -> List[Dict[str, Any]]:
        """
        Get the list of tools available in the MCP server.
        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing tool information.
        """
        tools_result = await self.session.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                }
            }
            for tool in tools_result.tools
        ]

    async def process_query(self, query: str, internet: bool) -> str:
        """
        Process a query using the MCP server.
        Args:
            query (str): The query to process.
            internet (bool): If False, internet_search tool will be disabled.
        Returns:
            str: The response from the MCP server.
        """
        print("Stage 0.1")
        tools = await self.get_mcp_tools()
        print("Stage 0.5")
        # if internet:
        #     system_context= "You are an assistant. Always search the internet to provide accurate, up-to-date answers. Use tools whenever facts are needed or you're unsure."
        # else:
        #     system_context = "You are an assistant. Internet access is disabled. Do not attempt internet search(strictly). Answer based on your existing knowledge or use other tools." #"You are an assistant. Use tools to provide accurate, up-to-date answers. Internet access is strictly disabled, do not attempt to search online even if asked instead answer it yourself based on your knowledge."
        if internet:
            system_context = (
                "User Country: India"
                "You are an assistant with access to specialized tools. "
                "Always search the internet to provide accurate, up-to-date answers. "
                "For weather forecasting, use the get_weather tool with the city name, current, forecast, days, forecast_type, and day_for_hourly values. "
                "days must always be greater than the day_for_hourly (day_for_hourly < days)"
            )
        else:
            system_context = (
                "User Country: India"
                "You are an assistant with access to specialized tools. Internet access is disabled. "
                "For weather forecasting, use the get_weather tool with the city name, current, forecast, days, forecast_type, and day_for_hourly values. "
                "days must always be greater than the day_for_hourly (day_for_hourly < days)"
            )
        is_bitcoin_query = any(term in query.lower() for term in ['bitcoin', 'btc', 'crypto']) and 'price' in query.lower()
    
        if is_bitcoin_query:
            query = f"{query}\n\nIMPORTANT: After getting the Bitcoin Open, High, and Low prices, you MUST use the get_bitcoin_price tool to predict the closing price using the ML model. Do not calculate it yourself."
        response = await self.GroqClient.chat.completions.create(
            model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_context,
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
            tools=tools,
            tool_choice="auto",
            max_completion_tokens=1024,
        )
        print("Stage 0")
        assistant_message = response.choices[0].message

        messages = [
            {"role": "user", "content": query},
            assistant_message
        ]
        print("Stage 1")
        if assistant_message.tool_calls:

            for tool_call in assistant_message.tool_calls:

                # Print the exact arguments being sent to the tool
                tool_arguments = json.loads(tool_call.function.arguments)
                print(f"Calling tool {tool_call.function.name} with arguments: {tool_arguments}")
                
                try:
                    result = await self.session.call_tool(
                        tool_call.function.name,
                        arguments=tool_arguments
                        # read_timeout_seconds=timedelta(seconds=30)  # Set a timeout for the tool call
                    )

                    # Print the raw result for debugging
                    # print(f"Raw tool result: {result}")
                    # print(f"Tool result content: {result.content}")
                    
                    # Convert dict to string if needed
                    tool_content = result.content[0].text
                    if isinstance(tool_content, dict):
                        tool_content = json.dumps(tool_content)
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_content
                    })
                except Exception as e:
                    print(f"Error calling tool {tool_call.function.name}: {e}")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": f"Error: {str(e)}"
                    })
                print(f"Tool call ID: {tool_call.function.name}\n")
                print(f"Tool call result: {result.content[0].text}\n")
            
            final_response = await self.GroqClient.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="none",
                max_completion_tokens=4096,
            )

            return final_response.choices[0].message.content
        
        return assistant_message.content
    
    async def cleanup(self) -> None:
        """
        Cleanup resources.
        """
        await self.exit_stack.aclose()


async def main():
    """
    Main function to run the MCP Groq client.   
    This function connects to the MCP server, processes a query, and prints the response.
    It also handles cleanup of resources.
    """
    try:
        print("Stage 33")
        client = MCPGroqClient(model="deepseek-ai/DeepSeek-V3")
        await client.connect_to_server()
        

        # query = "Tell me the day before yesterday in the format YYYY-MM-DD. and the day after tomorrow in the format YYYY-MM-DD. Also, tell me the current date in the format YYYY-MM-DD."
        query = input("Enter your query: ")
        print(f"Query: {query}\n")
        response = await client.process_query(query, internet = True)
        print(f"Response: {response}\n")
    except KeyboardInterrupt:
        print("Process interrupted by user.")
        await client.cleanup()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.cleanup()
        print("Cleanup completed.")

if __name__ == "__main__":
    asyncio.run(main())