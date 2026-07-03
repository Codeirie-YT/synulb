# synulb
A new programming language

This language is not complete as it is in Alpha v0.1.9.


To make a proposal on how this programming language should be, (although that really wont do much right now,) create a pull request in the SUP repo. (https://github.com/Codeirie-YT/SynulbUpdateProposals)


You must run Installer.py when you first download Synulb. Everytime you change the file location it has to run too.
The Installer currently only works on windows.

To run a synulb program (after running Installer.py), simply run:

synulb `<filename>`

Or just type synulb and it will prompt you for the filename.

```
$setup:
;

$main:
    >console: "Hello, World!\n";
;
```
Check out /ref for the versions and for the explanation of the language.
Check out /dev for the extension (called syn) and the example programs.

Latest major update: Alpha 0.1.9
This update fixes argument compilation, adds example programs, and also adds a vscode extension!

Example program for this version:

```
$setup:
    // This is for the 0.1.9 update
    @x:int;
;

$main:
    >console:"This command doesn't flush.\n", false;
    >console:"This command flushes.\n", true;
    >console:"This command also flushes\n";

    #x:10;
    >console:x;
;
```

This version also updates types.
Prev. major update: Alpha 0.1.8

Added printing vaiables and updated systems

Example program for this version:

```
$setup:
    @age: int;
;

$main:
    #age: 5;
    >console: "The age of Billy is...";
    >console: age;
;
```

