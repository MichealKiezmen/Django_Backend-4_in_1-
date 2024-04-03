import os

def delete_file_after_upload(current_file_path):
    if os.path.exists(current_file_path):
        os.remove(current_file_path)
        return True
    else:
        return False
