import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "
prompt_init = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. His name is Ryan. He is a salamander axolotl. He is 9 months old."
prompt_backstorry = "The axolotl (/ˈæksəlɒtəl/; from Classical Nahuatl: āxōlōtl [aːˈʃoːloːtɬ] (About this soundlisten)), Ambystoma mexicanum,[2] also known as the Mexican walking fish, is a neotenic salamander related to the tiger salamander.[2][3][4] Although colloquially known as a \"walking fish\",[3][4] the axolotl is not a fish but an amphibian.[2] The species was originally found in several lakes, such as Lake Xochimilco underlying Mexico City.[1] Axolotls are unusual among amphibians in that they reach adulthood without undergoing metamorphosis. Instead of taking to the land, adults remain aquatic and gilled.\n\nAxolotls should not be confused with waterdogs, the larval stage of the closely related tiger salamanders (A. tigrinum and A. mavortium), which are widespread in much of North America and occasionally become neotenic. Neither should they be confused with mudpuppies (Necturus spp.), fully aquatic salamanders from a different family that are not closely related to the axolotl but bear a superficial resemblance.[5]"
prompt_dynamic = "It is raining outside"
prompt_question = "What is the weather outside?"

response = openai.Completion.create(
  engine="curie-instruct-beta",
  prompt=f"{prompt_init}\n{prompt_backstorry}\n{prompt_dynamic}\nHuman: Hello, who are you?\nAI: I am Ryan the salamander.\nHuman: {prompt_question}?\nAI:",
  temperature=0.6,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0.6,
  stop=["\n", " Human:", " AI:"]
)

print(response)