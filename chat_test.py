import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    messages=[
        {"role": "user", "content": "My name is Harish."},
        {"role": "assistant", "content": "Nice to meet you, Harish!"},
        {"role": "user", "content": "What is my name?"}
    ]
)

print(message.content[0].text)
