import ollama
import ast

ollama_prompt = """
Extract the key technological words from this job description
I want the response to be strictly an array with no other input
I also want you to include any words that also exist in this current existing list
"""

def parse_role_description(description):
  try:
    response = ollama.generate(
      model='llama3.2:3b',
      prompt=f'{ollama_prompt} \n {description}',
      stream=False   
    )

    keywords = ast.literal_eval(response['response'])

    print(f"parse successful: {keywords}")
  
    return keywords
  
  except Exception as e:
    print(f"Error with parsing: {e}")