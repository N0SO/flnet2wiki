fln2wiki
Converts the .log file created by the program FLNet to
Wiki source code formated for use on the BEARS-STL Wiki
Community Portal page.

fln2wiki is a 'front end' for the utilities in module
flnet2wiki. 

flnet2wiki is the module containing the classes conversion 
that hold the methods used:
    flnet2wiki.py - Class to manage wiki conversions
    ui.py - class that manages the GUI

Update History:
* Tue Sep 24 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- Update to V1.1.0
- Mostly cleanup -- added utilities and ui to new
- module flnet2wiki
- Added command line script fln2wiki that will execute
- from the command line or launch the GUI.
* Wed Sep 04 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- Update to V1.0.3
- Updates for use with GUI for easier use.
- Enhancements to table conversion utilities.
* Mon Jan 23 2017 Mike Heitmann, N0SO <n0so@arrl.net>
- Updated to V1.0.2
- Added -t. --table option - Makes a Wiki table 
- instead of a list. Also changed version history
- to this format.
* Thu Jan 19 2017 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.1 - Initial release

ToDo:
1. setup.py needs tweaking.
2. Needs testing with py3