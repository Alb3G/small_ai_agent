from pathlib import Path
from functions.get_files_info import file_in_working_dir

def write_file(working_directory, file_path, content):
	if not file_in_working_dir(working_directory, file_path):
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

	base = Path(working_directory).resolve()
	target = base / file_path
	
	try:
		target.parent.mkdir(parents=True, exist_ok=True)
		
		target.write_text(content)
		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except PermissionError as p:
		return f'Error: {p.strerror}'
	except OSError as o:
		return f'Error: {o.strerror}'
	except TypeError as t:
		# El atributo 'strerror' no existe en TypeError. Puedes acceder al mensaje de error usando str(t)
		return f'Error: {str(t)}'
	except UnicodeEncodeError as u:
		return f'Error: {u.reason}'