import os 
import sys
import subprocess
import platform
from pathlib import Path



VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
GITIGNORE_FILE = ".gitignore"
Base_dir = Path.cwd()

DIRECTORIES = [
    "src",
    "tests",
    "docs", 
    "logs",
]

dependencies = [
    "requests==2.25.1",
    "Flask==3.1.2",
    "Django==6.0.1",
    "numpy==1.21.0",
    "pandas==1.3.0",
    "pytest==7.4.0",
    "black==23.9.1",
]
PATTERNS = [
    "*.log",        
    ".venv/",       # Virtual environment directories
    "__pycache__/", # Python cache files
    ".DS_Store",    # macOS system files
    "*.pyc",        # Compiled Python files
    ".env"          # Environment variable files
]

class Color:
    """Contains ANSI escape sequences for text formatting."""
    # Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # Reset
    RESET = '\033[0m' # Resets all formatting



def check_python_version():
    version = platform.python_version() 
    python_version =  ".".join(version.split(".")[:2])
    print(Color.BOLD + Color.GREEN + "Checking Python version..." + Color.RESET)
    print(Color.BOLD + Color.CYAN + f"current python version is : {Color.GREEN + python_version}" + Color.RESET)
    if float(python_version) < 3.08:
        print(Color.BOLD + Color.YELLOW + "Warning:" + Color.WHITE + " python version should be 3.8 or higher" + Color.RESET)
    print(Color.BOLD + Color.WHITE + "-"*30 + Color.RESET + "\n\n")
def create_venv():
    full_path = os.path.join(project_name,VENV_DIR)
    if os.path.exists(full_path):
        print(f"Virtual environment '{VENV_DIR}' already exists activating.....")
        return
    try:
        subprocess.run(args=[sys.executable ,"-m", "venv",full_path])
        print(f"virtual environment created")
    except subprocess.CalledProcessError as e:
        print(Color.RED + f"error creating virtual environment \n ERROR: {e}")
        sys.exit(1)
        
def create_directories():
   
    for directory in DIRECTORIES:
        full_path = os.path.join(project_name, directory)
        if os.path.exists(full_path):
            return
        else:
            os.makedirs(full_path,exist_ok=True)

def make_requirements_file(denpendencies=dependencies):
   file_path =os.path.join(project_name,REQUIREMENTS_FILE)
   if  os.path.exists(file_path):
        print(Color.BOLD + Color.GREEN + "updating requirement  file" + Color.RESET)
        try:
            with open(file_path, 'r') as f:
              existing_lines = f.readlines()
            existing_dep_names = set()
            for line in existing_lines:
               line=line.strip()
               if line and not line.startswith('#'):
                 dep_name = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                 existing_dep_names.add(dep_name)

            with open(file_path, 'a') as f:    
             for dep in dependencies:
                new_dep_name = dep.split('==')[0].split('>=')[0].split('<=')[0].strip()
                if new_dep_name not in existing_dep_names:
                        f.write(f"{dep}\n")
                        existing_dep_names.add(new_dep_name)
        except Exception as e:
            print(f"Exception occured while creating requirement.txt: {e}")
   else:
      print(Color.BOLD + Color.GREEN + "creating requirement  file" + Color.RESET)
      try:
          with open(file_path, 'a') as f:
           for dependancy in dependencies:  
            f.write(f"{dependancy}  \n")
      except Exception as e:
          print(f"Exception occured while creating requirement.txt: {e}")
              
def make_git_ignore_file():
    
    file_path = os.path.join(project_name, GITIGNORE_FILE)
    
    
    os.makedirs(project_name, exist_ok=True)

    try:
        existing_lines = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                # Read existing patterns, stripped of whitespace
                existing_lines = [line.strip() for line in f.readlines()]
        
        with open(file_path, 'a') as f:
            for pattern in PATTERNS:
                if pattern not in existing_lines:
                    f.write(f"{pattern}\n")
                   
                else:
                    pass
                    
    except Exception as e:
        print(f"Exception occurred while creating .gitignore: {e}")


def activate_venv():
    venv_dir  =os.path.join(project_name,VENV_DIR)
    if os.name == 'nt':  
        python_executable = os.path.join(venv_dir, "Scripts", "python.exe")
    else:  
        python_executable = os.path.join(venv_dir, "bin", "python")

    if not os.path.exists(python_executable):
        print(f"Error: Python executable not found at {python_executable}")
        sys.exit(1)

    try:
        if os.name != 'nt':
            os.execv(python_executable, [python_executable])
        else:
            subprocess.run([python_executable, "my_script.py"], check=True)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)   

def install_dependency():
    fullpath = os.path.join(project_name,REQUIREMENTS_FILE)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", fullpath])
        print(f"Successfully installed all dependencies from {fullpath}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during installation: {e}")
        sys.exit(1)
def run():
    subprocess.run("uvicorn project1/src/main : app --reload")

# if __name__ == "__main__":
global project_name 
project_name= input("Enter Project name: ")
check_python_version()
create_venv()
make_requirements_file()
activate_venv()
install_dependency()
create_directories()
make_git_ignore_file()
run()

