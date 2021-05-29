import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "
prompt_init = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. His name is Ryan. He is a salamander axolotl. He is 9 months old."
prompt_backstorry = ""
prompt_dynamic = "It is raining outside. The temperature is 21C. The current season is the fall. There is 15 persons looking at me. I feel safe."
prompt_past_conversation = ""
prompt_current_question = "Why being 9 months old make you feel safe?"

response = openai.Completion.create(
  engine="curie-beta",
  prompt=f"{prompt_init}\n{prompt_backstorry}\n{prompt_dynamic}\nHuman: Hello, who are you?\nAI: I am Ryan the salamander.\n{prompt_past_conversation}\nHuman: {prompt_current_question}?\nAI:",
  temperature=0.1,
  max_tokens=80,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=0.6,
  stop=["\n", " Human:", " AI:"]
)

print(response)