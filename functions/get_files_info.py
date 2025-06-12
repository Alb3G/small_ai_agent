import os
from constants import MAX_CHARS
from pathlib import Path

def is_directory(path):
	return os.path.isdir(path)

def file_in_working_dir(working_directory, directory):
	if directory is None or directory == ".":
		return True

	base = Path(working_directory).resolve()
	target = (base / directory).resolve()

	try:
		target.relative_to(base)
		return True
	except ValueError:
		return False

def get_files_info(working_directory, directory=None):
	if directory is None:
		directory = "."
		
	if not file_in_working_dir(working_directory, directory):
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

	target_dir_path = os.path.join(working_directory, directory)
	target_dir_abs_path = os.path.abspath(target_dir_path)

	if not is_directory(target_dir_abs_path):
		return f'Error: "{directory}" is not a directory'

	dir_files = os.listdir(target_dir_abs_path)

	for file in dir_files:
		file_path = os.path.join(target_dir_abs_path, file)

		try:
			file_size = os.path.getsize(file_path)
		except OSError as e:
			return f"Error: {e.strerror}"
		
		print(f"- {file}: file_size={file_size} bytes, is_dir={is_directory(file_path)}")