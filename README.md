# Documentation Search MCP Server

An MCP server that searches official documentation for LangChain, LlamaIndex, OpenAI, and uv. It uses Serper for web search and extracts readable page text before returning source links.

## Requirements

- Python 3.14 or newer
- uv
- A Serper API key

## Setup

Install the project dependencies:

```powershell
uv sync
```

Create a `.env` file in the project directory:

```env
SERVER_API=your_serper_api_key
```

Run a protocol smoke test:

```powershell
$request = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke-test","version":"1.0"}}}'
$request | uv run python .\mcp_server.py
```

The server uses the MCP `stdio` transport and should normally be started by an MCP-compatible client such as VS Code Copilot.

## VS Code configuration

Create `.vscode/mcp.json` with the following configuration, replacing the paths if the project is moved:

```json
{
	"servers": {
		"docs": {
			"type": "stdio",
			"command": "E:\\MCP_Python\\.venv\\Scripts\\python.exe",
			"args": ["E:\\MCP_Python\\mcp_server.py"],
			"env": {
				"SERVER_API": "${input:server-api-key}"
			}
		}
	},
	"inputs": [
		{
			"type": "promptString",
			"id": "server-api-key",
			"description": "Serper API key",
			"password": true
		}
	]
}
```

Start the `docs` server from **MCP: List Servers** in VS Code. Once it shows `Running`, ask Copilot to search a supported library, for example:

```text
Use the docs MCP tool to search OpenAI documentation for function calling.
```

Supported libraries are `langchain`, `llama-index`, `openai`, and `uv`.

## Security

Never commit `.env` or expose the Serper API key. The repository ignores `.env` by default.
