import os, sys, inspect
from ref.graphics import *
from time import sleep
from ProgramFiles.helper import v
from re import findall

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

def error(text: str):
    print('\n')
    print(f'\x1b[31m{text}')
    print('\x1b[37m')
    #exit()

def main():
    win = GraphWin("Synulb Installer Wizard", 500, 300)
    _format = Text(Point(60, 20), 'line format max 49 col (34 col self)'); _format.setSize(5); _format.draw(win)
    name = Text(Point(250, 150), f'Synulb Alpha'); name.setSize(30); name.setTextColor('thistle2'); name.draw(win)
    version = Text(Point(280, 170), v()[6:]); version.setTextColor('violetred'); version.draw(win)

    sleep(1)

    paragraph = Text(Point(250, 150), '''
This installer will create a command for synulb.
That way, you can run synulb programs like so:
synulb <programname>
In your terminal.

Do note that as of right now, you will need to 
run the installer everytime you move the SYNULB
file locaton.
(Click to Advance)''')
    paragraph.setSize(15)
    paragraph.draw(win)
    paragraph.setSize(10)
    win.getMouse()
    match sys.platform:
        case 'ios' | 'android':
            paragraph.setText("Why are you trying to run synulb on ios/android?\nIt wasn't meant for this.")
            win.getMouse()
            error("Synulb is not meant for this os, please stop it hurts")

        case 'aix':
            paragraph.setText("IBX AIX does not have installer support yet.")
            win.getMouse()
            error("IBM AIX does not have installer support yet.")

        case 'freebsd':
            paragraph.setText("FreeBSD does not have installer support yet.")
            win.getMouse()
            error("FreeBSD does not have installer support yet.")

        case 'darwin':
            paragraph.setText("Your OS may never get installer support.")
            win.getMouse()
            error("This OS may never get installer support yet.")

        case 'enscripten':
            paragraph.setText("Synulb is not meant to run on enscripten.")
            win.getMouse()
            error("Synulb is not meant to run on enscripten.")

    match os.name:
        case 'posix':
            paragraph.setText("Linux installer support is still in development.\nClick to (attempt) an installation.")
            win.getMouse()
            paragraph.move(0, -50)
            paragraph.setText("DETECTING CURRENT SHELL")
            sleep(0.5)

            # Check for shells, ask user which shells they would want to install synulb
            pshells = {'~/.bash_aliases'            : '!1 -- Bash (+Aliases)',
                       '~/.bashrc'                  : '!2 -- Bash', 
                       '~/.zshrc'                   : '!3 -- Z Shell', 
                       '~/.config/fish/config.fish' : '!4 -- Fish'}
            
            activeshells = []
            for file, sname in pshells.items():
                if os.path.exists(file):
                    activeshells.append(sname)

            if len(activeshells) == 0:
                paragraph.setText(f'No active shells detected. Please try again.\nCheck if any of these files exist:\n{'\n'.join(list(pshells.keys()))}')
                win.getMouse()
                error("Cannot Install on nothing")
            elif len(activeshells) == 1:
                installpoints = activeshells
            else:
                paragraph.setText(f'The following shells were detected.\nPlease type the number(s) (with the preceding "!")\n for the corresponding shell(s) you want to use for SYNULB.\nClick to Confirm\n\n{'\n'.join(activeshells)}')
                e = Entry(Point(250, 180), 10); e.draw(win)
                choice = e.getText()
                installpoints = list(list(pshells.keys())[x] for x in list(int(x[1:]) for x in findall(r'![0-9]', choice))) # list of digits found

            e.undraw()

            paragraph.setText("INSTALLING SYNULB FOR POSIX")
            if len(installpoints) == 0:
                paragraph.setText(f"Something went wrong. There are no valid installer points. Did you choose any correctly?")
                win.getMouse()
                error("NO VALID INSTALLER POINTS")
            else:
                for installpoint in installpoints:
                    paragraph.setText(f"INSTALLING SYNULB FOR POSIX//{(pshells[installpoint])[6:]} TO {installpoint}")
                    with open(installpoint, 'a') as installationIO:
                        if installationIO.writable():
                            pass
                        else:
                            paragraph.setText(f"Cannot write to installation point {installpoint} aka {(pshells[installpoint])[6:]}.\nClick to Continue Installation")
                            win.getMouse()

        case 'nt':
            paragraph.setText("Installing SYNULB FOR WINDOWS...")
            sleep(2.5)
            os.system(f'mkdir "C:\\SYNULBBAT"')
            os.system(f'(echo @echo off) > "C:\\SYNULBBAT\\synulb.bat"')
            os.system(f'(echo py "{get_script_dir()}\\ProgramFiles\\main.py" %*) >> "C:\\SYNULBBAT\\synulb.bat"')
            os.system(f'powershell -Command "[System.Environment]::SetEnvironmentVariable(\'Path\', $env:Path + \';C:\SYNULBBAT\', [System.EnvironmentVariableTarget]::User)"')
            paragraph.setText("> Sucessfully Installed!\nThe command can be found in \"C:\\SYNULBBAT\\synulb.bat\"\nIt has automatically been added to PATH.")
            win.getMouse()

        case 'java':
            paragraph.setText("JPython cannot access commands, meaning that a synulb command cannot be created on your device.")
            win.getMouse()
            error("Sorry, but JPython is not a supported interperter for Synulb. You will have to run ProgramFiles-main.py manually.")
    
    sleep(2)
    win.close()
    
if __name__ == '__main__':
    try:
        main()
    except GraphicsError:
        pass