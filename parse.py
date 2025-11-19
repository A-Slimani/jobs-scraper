import ollama

ollama_prompt = """
Extract the key technological words from this job description
I want it to be returned as an array
"""

def parse_role_description(description):
  response = ollama.generate(
    model='llama3.2:3b',
    prompt=f'{ollama_prompt} \n {description}'    
  )

  print(response['response'])