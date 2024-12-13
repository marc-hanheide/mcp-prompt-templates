from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def analyze_transcript(file_path: str):
    server_params = StdioServerParameters(
        command="python3",
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            try:
                # Read transcript file
                with open(file_path, 'r') as f:
                    transcript = f.read()
                print(f"Read transcript from {file_path}")
                
                # Get analysis
                result = await session.get_prompt(
                    "analyze-meeting",
                    arguments={"transcript": transcript}
                )
                
                # Print result
                for message in result.messages:
                    print(f"\n{message.content.text}")
                    
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(analyze_transcript("test_transcript.txt"))