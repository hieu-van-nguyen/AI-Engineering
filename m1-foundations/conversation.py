"""Message and Conversation dataclasses shaped like chat API payloads."""

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class Message:
    """A single immutable chat message."""

    role: str
    content: str


@dataclass
class Conversation:
    """An ordered list of messages."""

    messages: list[Message] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        """Append a new message to the conversation."""
        self.messages.append(Message(role=role, content=content))

    def to_dicts(self) -> list[dict[str, str]]:
        """Return messages as [{"role": ..., "content": ...}, ...] for chat APIs."""
        return [asdict(m) for m in self.messages]


if __name__ == "__main__":
    convo = Conversation()
    convo.add("user", "Hello!")
    convo.add("assistant", "Hi, how can I help?")
    print(convo.to_dicts())
