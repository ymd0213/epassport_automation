"""
Quick script to check your Chrome version
"""
import platform

def get_chrome_version():
    """Get Chrome browser version"""
    try:
        if platform.system() == "Windows":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            winreg.CloseKey(key)
            return version
    except:
        pass
    return None

if __name__ == "__main__":
    version = get_chrome_version()
    if version:
        major_version = version.split('.')[0]
        print(f"Chrome version: {version}")
        print(f"Major version: {major_version}")
    else:
        print("Could not detect Chrome version")

