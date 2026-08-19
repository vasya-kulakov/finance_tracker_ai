from openai import OpenAI

with open('apikeys.txt', 'r') as f:
    key = f.read().strip()
    
client = OpenAI(
  base_url="https://api.zveno.ai/v1",
  api_key=key,
)

completion = client.chat.completions.create(
  model="cohere/north-mini-code:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ],
)

print(completion.choices[0].message.content)