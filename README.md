pymlgame
========

pymlgame is an abstraction layer to easily build games for Mate Light inspired by pygame.

You need 3 parts to actually have a running game on Mate Light.

tl;dr
-----

```
virtualenv env
source env/bin/activate
python setup.py install
```

The game
--------

You can build a game using the pymlgame library. If you know the pygame library this should be nothing new to you.
Use the game_example.py to find out how to do so.

A controller
------------

If you want players, your game needs a controller to have some inputs. Controllers should work with every game made with
pymlgame. There is a controller_example.py to play with. An Android based controller app is in the works.

Mate Light
----------

To play pymlgames you need the awesome Mate Light. You could use the one on c-base space station, or build your own.
If you're not near c-base and don't want to build your own, you can use the Mate Light emulator provided with pymlgame.


Protocol
========

This is the coitus protocol that handles the communication between the game and the controllers.


Controller -> Game
------------------

### /controller/new/<port>

Connect a new controller to the game. Game will answer with /uid/<uid>. This is also known as 'anpymln'.

### /controller/<uid>/ping/<port>

Tell the game that the controller is still in use and update it's address and port. Use this once a minute or the
controller will get deleted.

### /controller/<uid>/kthxbye

Disconnect the controller properly. In theory you could just wait 60s but this is the cleaner way and most games would
be very happy if you use this.

###/controller/<uid>/states/<states>

Send the states of your controller keys. Always send all 14 states, even if your controller doesn't have 14 buttons.
The states should be an array with 0 for key not pressed and 1 for key pressed. So if you're pressing the Up button and
X the states array should look like this: 10000010000000
You can lookup all possible buttons and there location in the array in pymlgame/locals.py.

### /controller/<uid>/text/<text>

*Optional*

Send some text to the game. Maybe it asks you for a player name. Games should always give you the option to enter text
without this function but you can use it if your controller is capable of text input.


Game -> Controller
------------------

### /uid/<uid>

Tell the controller its uid. This is ideally an integer.

### /rumble/<duration>

*Optional*

Tell the controller to rumble. Duration should be given in milliseconds. Not all controllers have the ability to rumble.
Maybe they do it in an optical way.

### /message/<text>

*Optional*

Send some text to the controller. Be aware that not all controllers can display text, so don't send important things.

### /download/<url>

*Optional*

Tell the controller to download the media file under the given url. The game can then ask the controller to play the
file so that the player can hear some ingame sounds. Use this function everytime the game starts because a controller
could have deleted the files after playing. Controllers should ensure that files already downloaded gets downloaded
again to reduce loading times for games that have been played before.

### /play/<file>

*Optional*

Tell the controller to play the file with that name. Use the download command to download media files to the controller
before using this.


Tipps
-----

If your controller downloads media files for games it is good practice to delete the downloaded stuff from time to time
or give the user the ability to cleanup the downloaded files.

If your game uses some optional features, tell the players that they can have an even better gaming experience when they
use a controller with is capable of these features.


---

Have fun while playing pymlgames on Mate Light! :D
