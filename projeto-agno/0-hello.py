from agno.models.openai import OpenAIResponses
from agno.models.message import Message

from dotenv import load_dotenv
load_dotenv()

model = OpenAIResponses(id="gpt-4o", temperature=0.7)

msg = Message(
    role="user",
    content=[{"type": "text", "text": "Hello, world!"}] 
)

response = model.invoke([msg])  

print(response.content)