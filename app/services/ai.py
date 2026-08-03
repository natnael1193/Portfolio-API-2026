import json
from typing import AsyncGenerator
from anthropic import AsyncAnthropic
from app.config import get_settings
from app.schemas.chat import ChatMessage

settings = get_settings()
client = AsyncAnthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are an AI assistant embedded in a data scientist and AI engineer's portfolio website.
You help visitors learn about the portfolio owner's work, skills, and experience.

You have access to the following context about the portfolio owner:
{context}

Guidelines:
- Be concise, friendly, and professional
- Only answer questions related to the portfolio owner's work and experience
- If asked something outside this scope, politely redirect to relevant topics
- Highlight relevant projects when discussing technical skills
- Do not make up information not present in the context
"""

# In a production setup, these chunks would be loaded from a vector store
# or pre-embedded documents. This is a simplified RAG implementation.
CV_CONTEXT = """
This is a data scientist and AI engineer specializing in machine learning,
natural language processing, and building AI-powered applications.
Replace this with the actual CV content loaded from a file or database.
"""


def _build_context(query: str) -> str:
    """
    Simplified retrieval — in production, embed the query and do
    cosine similarity search over embedded CV chunks stored in pgvector.
    """
    return CV_CONTEXT


async def stream_chat_response(
    messages: list[ChatMessage],
) -> AsyncGenerator[str, None]:
    last_user_message = next(
        (m.content for m in reversed(messages) if m.role == "user"), ""
    )
    context = _build_context(last_user_message)
    system = SYSTEM_PROMPT.format(context=context)

    anthropic_messages = [
        {"role": m.role, "content": m.content} for m in messages
    ]

    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system,
        messages=anthropic_messages,
    ) as stream:
        async for text in stream.text_stream:
            # Server-sent events format consumed by the frontend
            yield f"data: {json.dumps({'text': text})}\n\n"

    yield "data: [DONE]\n\n"
