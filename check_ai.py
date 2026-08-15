from openai import OpenAI
client = OpenAI(
  base_url="https://api.zveno.ai/v1",
  api_key="sk-Ii5t4t7OOmLtmY6H61grwljoQLKrfMu11evY3ZNIqbg",
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