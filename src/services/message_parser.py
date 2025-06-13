from langchain_core.messages import AIMessage, ToolMessage, BaseMessage


def parse_agent_step(step) -> list[str]:
    messages = (
        step.get("reasoner", {}).get("messages", []) or
        step.get("messages", [])
    )

    chunks = []
    for msg in messages:
        if isinstance(msg, ToolMessage):
            chunks.append(f"[Tool Response] {msg.content}\n")
        elif isinstance(msg, AIMessage):
            if msg.content:
                chunks.append(f"[AI] {msg.content}\n")
            elif msg.tool_calls:
                for call in msg.tool_calls:
                    chunks.append(
                        f"[Tool Call] {call.get('name')} with input {call.get('input')}\n")
        elif isinstance(msg, BaseMessage) and getattr(msg, "content", None):
            chunks.append(f"{msg.content}\n")

    return chunks
