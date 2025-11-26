# Agent CLI Examples

> **Note:** These are conceptual examples demonstrating how to build AI agent CLIs with Llama Stack. They're designed for learning and prototyping, not production use.

This repository contains two simple CLI implementations that show how to create AI agents with file operation capabilities using Llama Stack and OpenShift AI 3.

## What's Included

- **`agent-cli.py`** - Basic interactive agent CLI with standard (non-streaming) responses
- **`agent-cli-streaming.py`** - Interactive agent CLI with real-time streaming responses
- **`tools.py`** - File operation tools (read, write, list directories)

Both CLIs give the agent access to file operations, allowing it to read files, write files, and list directory contents based on natural language requests.

## Requirements

- Python 3.12+
- Access to a Llama Stack server (e.g., OpenShift AI 3 or local instance)
- Llama Stack client library

## Installation

```bash
# Install dependencies
pip install llama-stack-client typer rich

# Set environment variables
export LLAMA_SERVER_URL="https://your-llama-stack-server.com"
export LLAMA_MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct"
```

## Usage

### Basic CLI (Non-streaming)

```bash
# Use defaults from environment variables
python agent-cli.py chat

# Override with CLI arguments
python agent-cli.py chat --model-name "meta-llama/Llama-3.1-70B-Instruct"
python agent-cli.py chat --server-url "http://localhost:8321"
```

### Streaming CLI (Real-time responses)

```bash
# Use defaults from environment variables
python agent-cli-streaming.py chat

# Override with CLI arguments
python agent-cli-streaming.py chat --system-prompt "You are a Python expert"
```

## Example Session

```
┌ Initialized ──────────────┐
│ Llama Stack Agent         │
└───────────────────────────┘
Session: cli-session-a7f3...
System: You are a helpful assistant.
Type 'exit' or 'quit' to end the session.

You: What Python files are in this directory?
Agent: I'll check the directory for you.

I found these Python files:
- agent-cli.py
- agent-cli-streaming.py
- tools.py

You: Read agent-cli.py and tell me what it does
Agent: I'll read that file for you.

This script creates an interactive CLI for chatting with a Llama Stack agent...
[continues with explanation]

You: exit
Goodbye!
```

## Key Differences

| Feature | agent-cli.py | agent-cli-streaming.py |
|---------|-------------|------------------------|
| Response style | Complete response after generation | Real-time streaming output |
| User experience | Wait for full response | See response as it generates |
| Dependencies | Basic Llama Stack client | Requires `AgentEventLogger` |
| Use case | Simple implementation | Better UX for longer responses |

## File Structure

```
.
├── agent-cli.py              # Basic non-streaming CLI
├── agent-cli-streaming.py    # Streaming CLI with real-time output
├── tools.py                  # File operation tools for the agent
└── README.md                 # This file
```

## How It Works

### The Agent

Both scripts create an agent using the Llama Stack API:

```python
agent = Agent(
    client,
    model=model,
    instructions=system_prompt,
    tools=[read_file, write_file, list_dir],
)
```

The agent can:
- Understand natural language requests
- Decide when to use file operation tools
- Execute functions and interpret results
- Provide helpful responses

### The Tools

Tools are simple Python functions with docstrings that the LLM reads to understand what they do:

```python
def read_file(file_path: str) -> str:
    """
    Reads a file and returns its contents.

    :param file_path: Path to the file to read.
    :return: The content of the file.
    """
    # Implementation...
```

The LLM uses these docstrings to decide when and how to call each function.

## Configuration Options

Both scripts support these options:

| Option | Environment Variable | Default | Description |
|--------|---------------------|---------|-------------|
| `--server-url` | `LLAMA_SERVER_URL` | Required | URL of your Llama Stack server |
| `--model-name` | `LLAMA_MODEL_NAME` | Required | Model identifier to use |
| `--system-prompt` | - | "You are a helpful assistant." | Instructions for the agent |

## Security Considerations

⚠️ **Important:** These are example scripts without security hardening.

Before using in any shared or production environment:

- **Sandbox file operations** - Limit access to specific directories
- **Validate inputs** - Sanitize all file paths and user input
- **Add authentication** - Don't expose without access controls
- **Audit logging** - Track all file operations
- **Rate limiting** - Prevent abuse

## Extending the Examples

### Add More Tools

```python
def search_files(pattern: str, directory: str = ".") -> list[str]:
    """
    Search for files matching a pattern.

    :param pattern: Glob pattern to match
    :param directory: Directory to search in
    :return: List of matching file paths
    """
    # Implementation...
```

Then add to the agent:

```python
agent = Agent(
    client,
    model=model,
    instructions=system_prompt,
    tools=[read_file, write_file, list_dir, search_files],
)
```

### Customize System Prompts

```bash
python agent-cli.py chat --system-prompt "You are an expert code reviewer. \
Focus on identifying bugs, security issues, and suggesting improvements."
```

## Troubleshooting

### Connection Errors

```
Error: Both LLAMA_SERVER_URL and LLAMA_MODEL_NAME must be set.
```

**Solution:** Set the required environment variables:

```bash
export LLAMA_SERVER_URL="https://your-server.com"
export LLAMA_MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct"
```

### Model Not Found

```
Error: Model not found on server
```

**Solution:** Check available models on your Llama Stack server or use a different model name.

### Import Errors

```
ModuleNotFoundError: No module named 'llama_stack_client'
```

**Solution:** Install dependencies:

```bash
pip install llama-stack-client typer rich
```

## Learn More

- **Llama Stack Documentation:** [https://llama-stack.readthedocs.io/](https://llama-stack.readthedocs.io/)
- **OpenShift AI 3:** [Red Hat OpenShift AI Documentation](https://docs.redhat.com/en/documentation/red_hat_ai/3)
- **Llama Stack Client Python:** [GitHub Repository](https://github.com/llamastack/llama-stack-client-python)

## License

These examples are provided as-is for educational purposes.

---

**Questions or improvements?** Feel free to open an issue or submit a pull request.
