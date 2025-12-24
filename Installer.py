import os, sys, inspect

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


match os.name:
    case 'posix':
        pass
    case 'nt':
        os.system(f'mkdir "C:\\SYNULBBAT"')
        os.system(f'(echo @echo off) > "C:\\SYNULBBAT\\synulb.bat"')
        os.system(f'(echo py "{get_script_dir()}\\ProgramFiles\\main.py" %*) >> "C:\\SYNULBBAT\\synulb.bat"')
        os.system(f'powershell -Command "[System.Environment]::SetEnvironmentVariable(\'Path\', $env:Path + \';C:\SYNULBBAT\', [System.EnvironmentVariableTarget]::User)"')
    case 'java':
        print("Sorry, but JPython is not a supported interperter for Synulb. You will have to run ProgramFiles-main.py manually.")