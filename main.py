import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from constants import SYSTEM_PROMPT
from functions.genai_schemas import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) <= 1:
	print("Error: No prompt added to the call")
	sys.exit(1)

user_prompt = sys.argv[1]
is_verbose = False

if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
	is_verbose = True

messages = [
	types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

# Available schemas
available_functions = types.Tool(
    function_declarations = [
        schema_get_files_info,
		schema_get_file_content,
		schema_write_file,
		schema_run_python
    ]
)

# Genai
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
	model = 'gemini-2.0-flash-001', 
	contents = messages,
	config = types.GenerateContentConfig(
		system_instruction = SYSTEM_PROMPT,
		tools = [available_functions]
	),
)

if response.function_calls:
	for func in response.function_calls:
		print(f"Calling function: {func.name}({func.args})")
else:
	print(response.text)

if is_verbose:
	print(f"User prompt: {user_prompt}")
	print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
	print(f"Response tokens: {response.usage_metadata.candidates_token_count}")