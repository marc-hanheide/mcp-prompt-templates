# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "anyio",
#     "mcp",
#     "pyyaml",
# ]
# ///
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
import yaml
import os
import asyncio

class TemplateServer(Server):
    def __init__(self):
        super().__init__("analysis-template-server")
        self.templates = self._load_templates()
    
    def _load_templates(self):
        templates = {}
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
        for category in os.listdir(template_dir):
            category_path = os.path.join(template_dir, category)
            if os.path.isdir(category_path):
                # Load config
                with open(os.path.join(category_path, 'config.yaml'), 'r') as f:
                    config = yaml.safe_load(f)
                
                # Load template
                with open(os.path.join(category_path, 'template.md'), 'r') as f:
                    template = f.read()
                
                templates[category] = {
                    'config': config,
                    'template': template
                }
        
        return templates

server = TemplateServer()

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    prompts = []
    for name, template in server.templates.items():
        prompts.append(
            types.Prompt(
                name=name,
                description=template['config']['description'],
                arguments=template['config']['arguments']
            )
        )
    return prompts

@server.get_prompt()
async def handle_get_prompt(
    name: str,
    arguments: dict[str, str] | None
) -> types.GetPromptResult:
    if name not in server.templates:
        raise ValueError(f"Unknown template: {name}")
    
    template = server.templates[name]
    formatted_template = template['template']
    
    # Replace placeholders with arguments
    if arguments:
        for key, value in arguments.items():
            formatted_template = formatted_template.replace(f"{{{{ {key} }}}}", value)
    
    return types.GetPromptResult(
        description=template['config']['description'],
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=formatted_template
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
                server_name="analysis-templates",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(run())