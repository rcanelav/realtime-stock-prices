from langchain_core.messages import AIMessage, BaseMessage, ToolMessage


def parse_agent_step(step) -> list[str]:
    messages = (
        step.get("reasoner", {}).get("messages", []) or
        step.get("messages", [])
    )

    chunks = []
    for msg in messages:
        content = msg.content

        if isinstance(msg, ToolMessage):
            chunks.append(f"[Tool Response] {content}\n")
        elif isinstance(msg, AIMessage):
            # Normalize content to string
            if isinstance(content, list):
                content = "".join(str(part)
                                  for part in content if isinstance(part, str))

            if content:
                for line in content.splitlines():
                    chunks.append(f"[AI] {line}\n")
            elif msg.tool_calls:
                for call in msg.tool_calls:
                    chunks.append(
                        f"[Tool Call] {call.get('name')} with input {call.get('input')}\n")
        elif isinstance(msg, BaseMessage) and content:
            if isinstance(content, list):
                content = "".join(str(part)
                                  for part in content if isinstance(part, str))
            chunks.append(f"{content}\n")

    return chunks
