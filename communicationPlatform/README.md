# Group-I Communication Component
A simple communication component used to configure round-robin-tournaments for turn based 2-player games to play 
locally and online. 
The component comes with a text based main menu used to setup and join games.

## Prerequisites
To run this module and associated tests you require the following tools installed on your machine
* [Python 3.7](https://www.python.org/downloads/release/python-370/)

## Tests
The module includes unittests to the internal major modules to ensure these run with fully functionality. 
To run the tests, navigate to the root folder of this repository and enter the following commands
```
python -m unittest tests/test_player.py
python -m unittest tests/test_tournament.py
```
## Use the module
If you wish to use this module you can simply implement a fitting Game Engine and Game Platform in 
[main.py](https://github.com/johanlovgren/Group-I). The intended locations in the code are marked with a 
 ``` # TODO ``` associated with a instructional comment.
