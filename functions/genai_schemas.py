from google.genai import types

# get_files_info schema
schema_get_files_info = types.FunctionDeclaration(
	name = "get_files_info",
	description = "Lists files in the specified directory along with their sizes, constrained to the working directory.",
	parameters = types.Schema(
		type = types.Type.OBJECT,
		properties = {
			"directory": types.Schema(
				type=types.Type.STRING,
				description = "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
			),
		},
	),
)

schema_get_file_content = types.FunctionDeclaration(
	name = "get_file_content",
	description = """
		This function resolves and validates a file path inside a given working directory, ensures it’s a regular file 
		within that directory, then reads and returns its contents—truncating and appending a notice if it exceeds the character limit.
	""",
	parameters = types.Schema(
		type = types.Type.OBJECT,
		properties = {
			"file_path": types.Schema(
				type = types.Type.STRING,
				description = "file_path is the relative path (from the working_directory) to the target file; it must point to a regular file (not a directory), otherwise an error is returned."
			)
		}
	)
)

schema_write_file = types.FunctionDeclaration(
	name = "write_file",
	description = "This function resolves and validates a target file path within the working directory, creates any necessary parent directories, writes the provided content to the file, and returns a success or error message.",
	parameters = types.Schema(
		type = types.Type.OBJECT,
		properties = {
			"file_path": types.Schema(
				type = types.Type.STRING,
				description = "file_path is the relative path (from the working_directory) to the target file; it must point to a regular file (not a directory), otherwise an error is returned."
			),
			"content": types.Schema(
				type = types.Type.STRING,
				description = "content is the string data to write into the target file; it’s written verbatim, and its length determines the character count reported in the success message."
			)
		},
	),
)

schema_run_python = types.FunctionDeclaration(
	name = "run_python_file",
	description = """
		run_python_file validates that the given path points to a `.py` file inside the working directory, then 
		executes it with a 30-second timeout—returning its stdout, stderr, or an error message.
	""",
	parameters = types.Schema(
		type = types.Type.OBJECT,
		properties = {
			"file_path": types.Schema(
				type = types.Type.STRING,
				description = "file_path is the relative path (from the working_directory) to the target file; it must point to a regular file (not a directory), otherwise an error is returned."
			)
		}
	)
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file,
    ]
)