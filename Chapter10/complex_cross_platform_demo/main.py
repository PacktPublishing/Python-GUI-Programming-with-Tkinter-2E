import platform
from backend import get_process_getter_class

os_name = platform.system()
os_backend = get_process_getter_class(os_name)()

print(os_backend.get_process_list())
