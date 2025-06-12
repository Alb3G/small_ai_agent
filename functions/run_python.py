from pathlib import Path
import subprocess
from functions.get_files_info import file_in_working_dir

def run_python_file(working_directory, file_path):
	if not file_in_working_dir(working_directory, file_path):
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

	base = Path(working_directory).resolve()
	target = base / file_path

	if not target.exists():
		return f'Error: File "{file_path}" not found.'
	
	if target.suffix != ".py":
		return f'Error: "{file_path}" is not a Python file.'
	
	try:
		result = subprocess.run(
            ["python", str(target)],
            timeout=30,
            capture_output=True,
            text=True,  # asegura strings, no bytes
			cwd=base
        )

		if result.stderr:
			return f'STDERR: {result.stderr}'
		
		if result.returncode != 0:
			return f'Process exited with code {result.returncode}'

		if not result.stdout:
			return f'No output produced.'
		
		return f'STDOUT: {result.stdout}'
	except subprocess.TimeoutExpired as e:
		return f"Error: executing Python file: {e.stderr}"
	except OSError as o:
		return f"Error: executing Python file: {o.strerror}"