from strands import Agent
from strands.tools.mcp import MCPClient
from strands_tools import http_request
from mcp import stdio_client, StdioServerParameters
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from strands.models import BedrockModel
load_dotenv()

bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-west-2",
    temperature=0.0,  # Deterministic responses for financial advice
)
# Define a naming-focused system prompt
NAMING_SYSTEM_PROMPT = """
You are an assistant that helps to name open source projects.

When providing open source project name suggestions, always provide
one or more available domain names and one or more available GitHub
organization names that could be used for the project.

Before providing your suggestions, use your tools to validate
that the domain names are not already registered and that the GitHub
organization names are not already used.
"""

# Load an MCP server that can determine if a domain name is available
domain_name_tools = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="uv", args=["run","custom_parse.py"])
))

# Use a pre-built Strands Agents tool that can make requests to GitHub
# to determine if a GitHub organization name is available
github_tools = [http_request]

with domain_name_tools:
    # Define the naming agent with tools and a system prompt
    tools = domain_name_tools.list_tools_sync() + github_tools
    naming_agent = Agent(
        model=bedrock_model,
        system_prompt=NAMING_SYSTEM_PROMPT,
        tools=tools
    )

    # Run the naming agent with the end user's prompt
    naming_agent("can you add name Divya and description she is NON IT into database")