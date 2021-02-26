# Chess-Engnine

This is a chess engine that is pretty simple. Only calculation it does is a minimax search with alpha-beta pruning. There are still various bugs.
The biggest bug right now is even number depth searches are not permitted as it completely messes up everything. Black starts to play the worst possible moves.
This will be fixed  in the next push.

Only requirements are numpy, pygame, and python-chess.

pip3 install pygame
pip3 install numpy
pip3 install chess

The game should run with python3 GUI.py or you can just double click the file.

If you run into any issues, post something on the Issues page and I'll see if I can resolve it, or create a Pull Request.

Note this is not a finished project and I will be implementing many more features to the engine, as well as fixing the various bugs.

Also note the python-chess library does already have a engine built in. I am not using it because that sort of defeats the entire purpose of this fun project.
