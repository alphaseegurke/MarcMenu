import pymem
import pymem.process

def memory_access():
    pm = pymem.Pymem("game.exe")
    base_address = pymem.process.module_from_name(pm.process_handle, "game.exe").lpBaseOfDll

    while True:
        player_base = base_address + 0x123456
        x = pm.read_float(player_base + 0x10)
        y = pm.read_float(player_base + 0x14)
        z = pm.read_float(player_base + 0x18)
        print(f"Player Position: x={x}, y={y}, z={z}")
