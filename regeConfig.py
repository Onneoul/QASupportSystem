import winreg
import traceback

def search_and_replace_key(hive, subkey, search, replace):
    try:
        with winreg.OpenKey(hive, subkey) as key:
            i = 0
            while True:
                try:
                    value_name, value_data, _ = winreg.EnumValue(key, i)
                    if search in str(value_data):
                        new_value_data = value_data.replace(search, replace)
                        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, new_value_data)
                        print(f"Modified: {subkey}\\{value_name} from {value_data} to {new_value_data}")
                    i += 1
                except OSError:
                    break

            i = 0
            while True:
                try:
                    new_subkey = winreg.EnumKey(key, i)
                    search_and_replace_key(hive, f"{subkey}\\{new_subkey}", search, replace)
                    i += 1
                except OSError:
                    break
    except PermissionError:
        print(f"PermissionError: Skipped {subkey}")
    except:
        traceback.print_exc()

if input("레지스트리를 수정하시겠습니까? (y/n): ").lower() == 'y':
    for hive, subkey in [
        (winreg.HKEY_LOCAL_MACHINE, ''), 
        (winreg.HKEY_CURRENT_USER, ''), 
        (winreg.HKEY_CLASSES_ROOT, ''),
        (winreg.HKEY_USERS, ''),
        (winreg.HKEY_CURRENT_CONFIG, '')
    ]:
        search_and_replace_key(hive, subkey, "원강식", "XIK")