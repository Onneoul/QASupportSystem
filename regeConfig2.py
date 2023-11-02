# -*- coding: utf-8 -*-
import winreg

def recursive_replace(hive, subkey, target, replacement):
    try:
        with winreg.OpenKey(hive, subkey, 0, winreg.KEY_WRITE | winreg.KEY_READ) as key:
            try:
                index = 0
                while True:
                    # Enumerate values
                    value_name, value_data, value_type = winreg.EnumValue(key, index)
                    changed = False
                    
                    # Check for the target string in value name
                    if target in value_name:
                        new_value_name = value_name.replace(target, replacement)
                        winreg.SetValueEx(key, new_value_name, 0, value_type, value_data)
                        winreg.DeleteValue(key, value_name)
                        changed = True
                    
                    # Check for the target string in value data (only for strings and expandable strings)
                    if value_type in (winreg.REG_SZ, winreg.REG_EXPAND_SZ) and target in str(value_data):
                        new_value_data = value_data.replace(target, replacement)
                        winreg.SetValueEx(key, value_name, 0, value_type, new_value_data)
                        changed = True
                    
                    if not changed:
                        index += 1
                    
            except WindowsError:
                # Enumeration complete
                pass

            # Now recursively apply for all subkeys
            index = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, index)
                    recursive_replace(hive, f"{subkey}\\{subkey_name}", target, replacement)
                    index += 1
                except WindowsError:
                    # Enumeration complete
                    break

    except WindowsError:
        # Key does not exist or some other error
        pass

# Define the hives to process
hives = [winreg.HKEY_CLASSES_ROOT, winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE,
         winreg.HKEY_USERS, winreg.HKEY_PERFORMANCE_DATA, winreg.HKEY_CURRENT_CONFIG,
         winreg.HKEY_DYN_DATA]

# Perform the replacement
for hive in hives:
    recursive_replace(hive, "", "원강식", "XIK")