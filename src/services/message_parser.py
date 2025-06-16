import json
from dataclasses import asdict

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from structlog import get_logger

from src.models.models import AgentDisplayConfig

logger = get_logger()


def parse_agent_step(step: dict, config: AgentDisplayConfig) -> list[str]:
    chunks = []

    logger.bind(step=step, config=asdict(config)).debug("⚡ Parsing agent step")
    for node_name, node_output in step.items():
        if not isinstance(node_output, dict) or "messages" not in node_output:
            logger.warning("⚠️ Skipping node with unexpected output", node=node_name)
            continue

        for msg in node_output["messages"]:
            chunks += _format_msg(msg, prefix=f"data: [{node_name.upper()}]", config=config)

    return chunks


def _format_msg(msg, prefix: str, config: AgentDisplayConfig) -> list[str]:
    chunks = []
    content = msg.content

    if isinstance(content, list):
        content = "".join(
            part["text"]
            for part in content
            if isinstance(part, dict) and "text" in part
        )

    if isinstance(msg, ToolMessage) and config.show_tool_responses:
        chunks.append(f"{prefix} [Tool Response] {content}\n")

    elif isinstance(msg, AIMessage):
        if config.show_ai_messages and content:
            for line in content.splitlines():
                chunks.append(f"{prefix} [AI] {line}\n")

        if config.show_tool_calls and msg.tool_calls:
            for call in msg.tool_calls:
                name = call.get("name")
                input_str = json.dumps(call.get("input"), indent=2)
                chunks.append(f"{prefix} [Tool Call] {name} with input {input_str}\n")

    elif isinstance(msg, BaseMessage) and content and config.show_base_messages:
        chunks.append(f"{prefix} {content}\n")

    return chunks
