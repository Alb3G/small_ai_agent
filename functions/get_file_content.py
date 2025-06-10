import os
from functions.get_files_info import is_directory, file_in_working_dir
from constants import MAX_CHARS

def reach_limit(file_path, max_chars=10000):
	# Analizar si deberiamos retornar esto también como string para darle contexto al agente.
	try:
		size = os.path.getsize(file_path)
		return size > max_chars
	except OSError as e:
		return False

def get_file_content(working_directory, file_path):
	working_directory_abs_path = os.path.abspath(working_directory)
	target_file_path = os.path.join(working_directory_abs_path, file_path)
	
	if not os.path.exists(target_file_path) or is_directory(target_file_path):
		return f'Error: File not found or is not a regular file: "{file_path}"'

	if not file_in_working_dir(working_directory, file_path):
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	
	limit_file_content = reach_limit(target_file_path)
	file_content = ""
	with open(target_file_path, "r") as f:
		if limit_file_content:
			file_content = f.read(MAX_CHARS)
			file_content += f'\n[...File "{file_path}" truncated at 10000 characters]'
		else:
			file_content = f.read()
	

	return file_content