import sys
import subprocess
import os
from pathlib import Path

def creating_venv(venv_name="venv"):
    """Create a virtual environment"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "venv", venv_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Virtual environment '{venv_name}' created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e.stderr}")
        return False

def install_flask(venv_name="venv"):
    """Install Flask in the virtual environment"""
    pip_path = get_pip_path(venv_name)
    
    try:
        result = subprocess.run(
            [pip_path, "install", "flask"],
            capture_output=True,
            text=True,
            check=True
        )
        print("Flask installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing Flask: {e.stderr}")
        return False

def get_pip_path(venv_name="venv"):
    """Get the path to pip within the virtual environment"""
    if sys.platform == "win32":
        return os.path.join(venv_name, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_name, "bin", "pip")

def get_activate_command(venv_name="venv"):
    """Return the activation command based on platform"""
    if sys.platform == "win32":
        return f"{venv_name}\\Scripts\\activate"
    else:
        return f"source {venv_name}/bin/activate"

def appFile():
    """Create the Flask app file"""
    try:
        content = """from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "Palambing Please"

if __name__ == "__main__":
    app.run(debug=True)
"""
        with open("app.py", "w") as file:
            file.write(content)
        print("app.py created successfully")
        return True
    except Exception as e:
        print(f"Error creating app.py: {e}")
        return False

def print_help():
    """Display help information"""
    print("Usage: python flask_startup.py [options]")
    print()
    print("Options:")
    print("  -start [venv_name]    Create virtual environment and setup Flask (default: venv)")
    print("  -die                  Show deactivation command")
    print("  -h, --help            Show this help message")
    print()
    print("Note: After running -start, you need to activate the virtual environment yourself:")
    print(f"      {get_activate_command()}")

def main(venv_name="venv"):
    """Main function to set up the Flask environment"""
    if not creating_venv(venv_name):
        return False
        
    if not install_flask(venv_name):
        return False
        
    if not appFile():
        return False
        
    print("\nSetup completed! Next steps:")
    print(f"1. Activate the virtual environment: {get_activate_command(venv_name)}")
    print("2. Run: python app.py or flask run")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help", "kupal"):
        print_help()
    elif sys.argv[1] == "-start":
        venv_name = sys.argv[2] if len(sys.argv) > 2 else "venv"
        main(venv_name)
    elif sys.argv[1] == "-die":
        print("To deactivate the virtual environment, simply run: deactivate")
    else:
        print("Invalid option. Use -h for help.")