from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
import asyncio
import anthropic

class MeetingAnalysisServer(Server):
    def __init__(self):
        super().__init__("meeting-analysis-server")
        # Initialize Claude client
        self.claude = anthropic.Anthropic()

    async def analyze_with_claude(self, transcript: str) -> str:
        message = await self.claude.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0,
            system="You are an Executive Assistant working for a global infrastructure consultancy.",
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this meeting transcript and provide a structured summary:\n\n{transcript}"
                }
            ]
        )
        return message.content

server = MeetingAnalysisServer()

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="analyze-meeting",
            description="Analyze meeting transcript",
            arguments=[
                types.PromptArgument(
                    name="transcript",
                    description="The meeting transcript to analyze",
                    required=True
                )
            ]
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str,
    arguments: dict[str, str] | None
) -> types.GetPromptResult:
    if name != "analyze-meeting":
        raise ValueError(f"Unknown prompt: {name}")
    
    transcript = arguments.get("transcript", "")
    
    # Get analysis from Claude
    analysis = await server.analyze_with_claude(transcript)
    
    return types.GetPromptResult(
        description="Meeting analysis",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=analysis
                )
            )
        ]
    )

async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="meeting-analysis",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(run())