import os
import sys
import argparse
from pathlib import Path

def get_startup_dir() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise ValueError("APPDATA environment variable not found. Cannot configure Windows startup.")
    return Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

def install():
    startup_dir = get_startup_dir()
    bat_path = startup_dir / "JARVIS_Startup.bat"
    
    project_dir = Path(__file__).parent.resolve()
    
    # Check if a .venv exists, otherwise use current python executable
    venv_python = project_dir / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        python_exe = str(venv_python)
    else:
        python_exe = sys.executable
    
    # We use a standard batch script to launch JARVIS in the background (or foreground).
    # Since it's a voice assistant, keeping a console window is often fine or we can launch it minimizing.
    # To launch silently we could use pythonw, but regular python is fine as a terminal window.
    bat_content = f"""@echo off
cd /d "{project_dir}"
"{python_exe}" run.py
"""
    bat_path.write_text(bat_content, encoding="utf-8")
    print(f"JARVIS startup script installed successfully at:\n{bat_path}")
    print("JARVIS will now automatically start when you log into Windows.")

def uninstall():
    startup_dir = get_startup_dir()
    bat_path = startup_dir / "JARVIS_Startup.bat"
    if bat_path.exists():
        bat_path.unlink()
        print("JARVIS startup script removed successfully.")
    else:
        print("JARVIS startup script not found. It is already disabled.")

def status():
    startup_dir = get_startup_dir()
    bat_path = startup_dir / "JARVIS_Startup.bat"
    if bat_path.exists():
        print(f"JARVIS is configured to start on login.\nPath: {bat_path}")
    else:
        print("JARVIS is NOT configured to start on login.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage JARVIS Windows Auto Start.")
    parser.add_argument("--disable", action="store_true", help="Disable JARVIS startup")
    parser.add_argument("--status", action="store_true", help="Check JARVIS startup status")
    
    args = parser.parse_args()
    
    try:
        if args.status:
            status()
        elif args.disable:
            uninstall()
        else:
            install()
    except Exception as e:
        print(f"Error configuring JARVIS startup: {e}")
