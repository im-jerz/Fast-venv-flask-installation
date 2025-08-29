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
        content = """from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    message = "Palambing Please"
    return render_template("index.html", message=message)

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


def htmlFile():
    try:
        content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>{{message}}</h1>
    <script src="{{ url_for('static', filename='js/index.js') }}"></script>
</body>
</html>
"""
        with open("templates/index.html", "w") as file:
            file.write(content)
        print("index.html created successfully")
        return True
    except Exception as e:
        print(f"Error creating index.html: {e}")
        return False
    
def cssFile():
    try:
        content = """
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
"""
        with open("static/css/style.css", "w") as file:
            file.write(content)
        print("style.css created successfully")
        return True
    except Exception as e:
        print(f"Error creating style.css: {e}")
        return False
    
def jsFile():
    try:
        content = """
console.log("Hello World");
"""
        with open("static/js/index.js", "w") as file:
            file.write(content)
        print("index.js created successfully")
        return True
    except Exception as e:
        print(f"Error creating index.js: {e}")
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
    folder = Path(venv_name)

    if not folder.exists():
        os.makedirs("templates", exist_ok=True)
        os.makedirs("static/css", exist_ok=True)
        os.makedirs("static/js", exist_ok=True)
        if not creating_venv(venv_name):
            return False
            
        if not install_flask(venv_name):
            return False
            
        if not appFile():
            return False
        
        if not htmlFile():
            return False
        
        if not cssFile():
            return False
        
        if not jsFile():
            return False
            
        print("\nSetup completed! Next steps:")
        print(f"1. Activate the virtual environment: {get_activate_command(venv_name)}")
        print("2. Run: python app.py or flask run")
        return True
    else:
        print(f"You have a folder name '{venv_name}' already exists.")

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        print_help()
    elif sys.argv[1] == "-start":
        venv_name = sys.argv[2] if len(sys.argv) > 2 else "venv"
        main(venv_name)
    elif sys.argv[1] == "-die":
        print("To deactivate the virtual environment, simply run: deactivate")
    else:
        print("Invalid option. Use -h for help.")