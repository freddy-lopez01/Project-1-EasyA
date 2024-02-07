# Project-1-EasyA


EasyA that students can use to figure out which professors in which classes are giving the most As, and which professors are giving the fewest Ds or Fs.
The system could help students to an “easy A” or make sure that they “just pass”. The system will use grade data from 2013-2016 at the University of Oregon.

(a) Within a single graph, broken out by instructor for:
(1) A single class (such as “Math 111”).
(2) A single department (such as “Math”).
(3) All classes of a particular level within a department (such as all “Math 100-level” classes,
from 100-level classes through 600-level classes).

Programming Constraints
• The system may be built using Python 3 along with The Python Standard Library https://
docs.python.org/3/library/index.html, but no other imports except for:
mysql, pymongo, and matplotlib
This means that the only GUI package that can be used is tkinter.

• Python code must run in Python 3.10 through 3.12.
• The system may be built using Java and Java Standard Edition modules, no other imports.
• The system may be built in C/C++, the C++ standard library, Cocoa, and no other components.
• Java code must run in Java 19 or 20.
• Instructions must be provided for how to compile the code.
• No server connections may be required for either installing or running the software, except for
setting up mysql on ix, and you must provide instructions on how to set this up. The
instructions should be as the MongoDB and MySQL guidance at
https://systems.cs.uoregon.edu/wiki/index.php?n=Help.Tools
(along with whatever files are need to create your tables and such)

• No virtual environments may be required to run your projects.
• No gaming engines such as Unity may be required to run your projects.

There can be at most 20 user actions to compile the code and run the program.
• An experienced computer programmer should not require more than 30 minutes working alone
with the submitted materials to compile and run the code.



The following document describes the modules and corresponding code artifacts for the EasyA Grade Graphing Comparison application. This document was written for the Computer Science 422 Software Methodologies Project 1 assignment for future adjustments/expansions. It discusses the codebase with its corresponding files and functions contained within.
All code was written using a multitude of interactive development environments such as VS Code, Pycharm, Iterm, and Neovim.
This documentation assumes a fundamental knowledge of the Python programming language, Python Libraries MatPlotLib, Numpy, Tkinter, & MySQL specifically SQLite3.
Please refer to the Installation instructions for setting up dependencies, and the User manual for how the program is currently set up regarding user inputs.
