# synulb
A new programming language


This language is not complete as it is in Alpha v0.1.8_a.


To make a proposal on how this programming language should be, (although that really wont do much right now,) create a pull request in the SUP repo. (https://github.com/Codeirie-YT/SynulbUpdateProposals)


You must run Installer.py when you first download Synulb. Everytime you change the file location it has to run too.
The Installer currently only works on windows.

To run a synulb program (after running Installer.py), simply run:

synulb `<filename>`

Or just type synulb and it will prompt you for the filename.

So far, only the hello world program works:

```
$setup:
;

$main:
    >console: "Hello, World!";
;
```

Latest major update: Alpha 0.1.8

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

Latest minor update: Alpha 0.1.8_a

Updated version no. and fixed formatting issue

Latest minorest update: Alpha 0.1.8_ab

Added synulb as a language in github