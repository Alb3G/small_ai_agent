import os

def is_directory(path):
	return os.path.isdir(path)

def file_in_working_dir(working_directory, directory):
	if directory is None or directory == ".":
		return True

	working_directory_abs_path = os.path.abspath(working_directory)
	wd_files =  os.listdir(working_directory_abs_path)

	for file in wd_files:
		if file == directory:
			return True
	
	return False

def get_files_info(working_directory, directory=None):
	# Que pasa si directory es None porque no se le pasa ningun argumento????
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

def get_file_content(working_directory, file_path):
	if not file_in_working_dir(working_directory, file_path):
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'