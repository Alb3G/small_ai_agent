import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def generate_content_type(function_name, function_result):
	return types.Content(
				role="tool",
				parts=[
					types.Part.from_function_response(
						name=function_name,
						response={"result": function_result},
					)
				],
			)

def call_function(function_call_part, verbose=False):
	function_name = function_call_part.name
	function_args = function_call_part.args
	function_args["working_directory"] = "./calculator"

	if verbose:
		print(f"Calling function: {function_name}({function_args})")
	else:
		print(f" - Calling function: {function_name}")

	match function_name:
		case "get_files_info":
			function_result = get_files_info(**function_args)
			generate_content_type(function_name, function_result)
		case "get_file_content":
			function_result = get_file_content(**function_args)
			generate_content_type(function_name, function_result)
		case "write_file":
			function_result = write_file(**function_args)
			generate_content_type(function_name, function_result)
		case "run_python_file":
			function_result = run_python_file(**function_args)
			generate_content_type(function_name, function_result)
		case _:
			return types.Content(
				role="tool",
				parts=[
					types.Part.from_function_response(
						name=function_name,
						response={"error": f"Unknown function: {function_name}"},
					)
				],
			)