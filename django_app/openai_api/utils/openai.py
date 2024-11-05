import re

from openai import OpenAI
from openai.types.beta.threads import Message

from django_app.core.settings import API_KEY_OPENAI, ASSISTANT_ID

client = OpenAI(api_key=API_KEY_OPENAI)
assistant_id = ASSISTANT_ID


def request_to_gpt(message: str, name_model: str) -> str:
    completion = client.chat.completions.create(
        model=name_model,
        messages=[{
            "role": "user",
            "content": message
        }]
    )

    return completion.choices[0].message.content


def extraction_data_from_answer_assistant(data_from_assistant: list[Message]) -> str:
    for message in data_from_assistant:
        if message.role == "assistant":
            text = message.content[0].text.value
            cleaned = re.sub("【.*?†source】", "", text)

            return cleaned.strip().replace("\n", "")


def openai_assistant() -> str:
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="message"
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions="Instructions for assistant"
    )
    if run.status == "completed":
        get_message = client.beta.threads.messages.list(
            thread_id=thread.id,
        )
    else:
        return "An error occurred"

    return extraction_data_from_answer_assistant(get_message.data)
