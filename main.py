import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from constants import SYSTEM_PROMPT
from functions.genai_schemas import *
from functions.call_function import call_function

def main():
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")

	if len(sys.argv) <= 1:
		print("Error: No prompt added to the call")
		sys.exit(1)

	user_prompt = sys.argv[1]
	is_verbose = False

	if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
		is_verbose = True

	contents = [
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
	generate_content(client, contents, is_verbose, available_functions)

def generate_content(client, contents, is_verbose, available_functions):
	response = client.models.generate_content(
		model = 'gemini-2.0-flash-001', 
		contents = contents,
		config = types.GenerateContentConfig(
			system_instruction = SYSTEM_PROMPT,
			tools = [available_functions]
		),
	)

	if is_verbose:
		print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
		print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

	if not response.function_calls:
		return response.text
	
	function_responses = []

	for func_call in response.function_calls:
		function_call_result = call_function(func_call, verbose=is_verbose)
		
		if (
			not function_call_result.parts
			or not function_call_result.parts[0].function_response
		):
			raise Exception("empty function call result")
		
		if is_verbose:
			print(f"-> {function_call_result.parts[0].function_response.response}")
		
		function_responses.append(function_call_result.parts[0])

		if not function_responses:
			raise Exception("no function responses generated, exiting.")

if __name__ == "__main__":
	main()