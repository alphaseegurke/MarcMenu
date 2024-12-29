import ctypes
import psutil

def get_process_pid(process_name):
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

def inject_dll(process_name, dll_path):
    pid = get_process_pid(process_name)
    if not pid:
        print(f"Process {process_name} not found.")
        return False

    PROCESS_ALL_ACCESS = 0x1F0FFF
    dll_path_bytes = dll_path.encode('utf-8')

    # Open process
    process = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process:
        print("Failed to open process.")
        return False

    # Allocate memory
    dll_path_address = ctypes.windll.kernel32.VirtualAllocEx(process, 0, len(dll_path_bytes), 0x3000, 0x40)
    if not dll_path_address:
        print("Failed to allocate memory.")
        return False

    # Write DLL path into process memory
    written = ctypes.c_size_t()
    ctypes.windll.kernel32.WriteProcessMemory(process, dll_path_address, dll_path_bytes, len(dll_path_bytes), ctypes.byref(written))

    # Get LoadLibraryA address
    kernel32 = ctypes.windll.kernel32.GetModuleHandleA(b"kernel32.dll")
    load_library = ctypes.windll.kernel32.GetProcAddress(kernel32, b"LoadLibraryA")

    # Create remote thread to load DLL
    thread = ctypes.windll.kernel32.CreateRemoteThread(process, None, 0, load_library, dll_path_address, 0, None)
    if not thread:
        print("Failed to create remote thread.")
        return False

    print("DLL successfully injected!")
    return True
