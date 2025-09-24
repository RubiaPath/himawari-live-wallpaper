#!/usr/bin/env python3
"""
CLI for Himawari Wallpaper

Provides commands to install/uninstall LaunchAgent, run wallpaper update once,
or restore the system default wallpaper.
"""

import os
import sys
import subprocess
import getpass
from pathlib import Path

HOME = Path.home()
AGENT_NAME = "com.himawari-live-wallpaper"
PLIST_PATH = HOME / f"Library/LaunchAgents/{AGENT_NAME}.plist"
SCRIPT_PATH = Path(__file__).parent / "himawari_wallpaper.py"
VENV_PATH = Path(__file__).parent / ".venv"
VENV_PYTHON = VENV_PATH / "bin/python3"

def create_venv():
    """Create virtual environment and install dependencies (only once)."""
    if not VENV_PATH.exists():
        print("🌱 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_PATH)], check=True)
        print("📦 Installing dependencies...")
        subprocess.run([str(VENV_PYTHON), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(VENV_PYTHON), "-m", "pip", "install", "-r", str(Path(__file__).parent / "requirements.txt")], check=True)
    else:
        print("✅ Virtual environment already exists. Skipping creation.")


def install_agent():
    """Install LaunchAgent to run himawari_wallpaper.py every 10 minutes."""
    create_venv()
    username = getpass.getuser()
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{AGENT_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{VENV_PYTHON}</string>
        <string>-u</string>
        <string>{SCRIPT_PATH}</string>
    </array>
    <key>StartInterval</key>
    <integer>600</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/{username}/Library/Logs/{AGENT_NAME}.out</string>
    <key>StandardErrorPath</key>
    <string>/Users/{username}/Library/Logs/{AGENT_NAME}.err</string>
</dict>
</plist>
"""
    PLIST_PATH.write_text(plist_content)
    subprocess.run(["launchctl", "load", str(PLIST_PATH)], check=True)
    print(f"✅ LaunchAgent installed: {AGENT_NAME}")


def uninstall_agent():
    """Unload and remove LaunchAgent."""
    if PLIST_PATH.exists():
        subprocess.run(["launchctl", "unload", str(PLIST_PATH)], check=False)
        PLIST_PATH.unlink()
        print("🛑 LaunchAgent uninstalled")


def run_once():
    """Run himawari_wallpaper.py once manually."""
    subprocess.run([str(VENV_PYTHON), str(SCRIPT_PATH)], check=True)


def restore_wallpaper():
    """Restore system default wallpaper."""
    script = '''
    tell application "System Events"
        set desktopCount to count of desktops
        repeat with desktopNumber from 1 to desktopCount
            tell desktop desktopNumber
                set picture to (path to pictures folder as string) & "DefaultDesktop.jpg"
            end tell
        end repeat
    end tell
    '''
    subprocess.run(["osascript", "-e", script])
    print("🔄 Wallpaper restored to default")


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py [install|runonce|stop|restore]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "install":
        install_agent()
        run_once()
    elif cmd == "runonce":
        run_once()
    elif cmd == "stop":
        uninstall_agent()
    elif cmd == "restore":
        restore_wallpaper()
    else:
        print("Unknown command")
        sys.exit(1)


if __name__ == "__main__":
    main()
