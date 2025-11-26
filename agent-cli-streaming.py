"""
Interactive CLI for chatting with Llama Stack Agent with streaming responses.

Usage:
    python agent-cli-streaming.py chat
    python agent-cli-streaming.py chat --system-prompt "You are a coding assistant"

Environment Variables:
    LLAMA_SERVER_URL - URL of the Llama Stack server
    LLAMA_MODEL_NAME - Model to use (e.g., 'llama-3.1-8b')
"""
import os
import uuid
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger
from tools import read_file, write_file, list_dir

app = typer.Typer()
console = Console()


@app.command()
def chat(
    system_prompt: str = typer.Option(
        "You are a helpful assistant.",
        help="The system prompt/instructions for the agent."
    ),
    server_url: str = typer.Option(
        None,
        help="Llama Stack Server URL. Defaults to LLAMA_SERVER_URL env var."
    ),
    model_name: str = typer.Option(
        None,
        help="Model name to use. Defaults to LLAMA_MODEL_NAME env var."
    ),
) -> None:
    """
    Start an interactive chat session with streaming responses.

    The agent has access to file operations: read_file, write_file, and list_dir.
    Responses are streamed in real-time as they're generated.
    Type 'exit' or 'quit' to end the session.
    """
    # Get configuration from CLI args or environment variables
    url = server_url or os.environ.get("LLAMA_SERVER_URL")
    model = model_name or os.environ.get("LLAMA_MODEL_NAME")

    if not url or not model:
        console.print("[bold red]Error:[/bold red] Both LLAMA_SERVER_URL and LLAMA_MODEL_NAME must be set.")
        raise typer.Exit(code=1)

    try:
        # Initialize client and agent with file operation tools
        client = LlamaStackClient(base_url=url)
        agent = Agent(
            client,
            model=model,
            instructions=system_prompt,
            tools=[read_file, write_file, list_dir],
        )

        # Create a unique session for this chat
        session_id = agent.create_session(session_name=f"cli-session-{uuid.uuid4()}")

        console.print(Panel.fit("[bold green]Llama Stack Agent (Streaming)[/bold green]", title="Initialized"))
        console.print(f"[dim]Session: {session_id}[/dim]")
        console.print(f"[bold blue]System:[/bold blue] {system_prompt}")
        console.print("[dim]Type 'exit' or 'quit' to end the session.[/dim]\n")

        # Main chat loop
        while True:
            user_input = Prompt.ask("[bold yellow]You[/bold yellow]")

            if user_input.lower() in ["exit", "quit"]:
                console.print("[bold green]Goodbye![/bold green]")
                break

            if not user_input.strip():
                continue

            try:
                # Prepare message in the format expected by create_turn
                messages = [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]

                console.print("[bold cyan]Agent:[/bold cyan] ", end="")

                # Stream response with event logging
                event_logger = AgentEventLogger()

                for chunk in agent.create_turn(
                    messages=messages,
                    session_id=session_id,
                    stream=True
                ):
                    # Log the event - AgentEventLogger formats the chunks
                    for log_msg in event_logger.log([chunk]):
                        console.print(log_msg, end="", markup=False)

                console.print("\n")  # New line after response

            except (IndexError, AttributeError) as e:
                console.print(f"[bold red]Error:[/bold red] Invalid response format: {e}")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Session interrupted.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Fatal Error:[/bold red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
