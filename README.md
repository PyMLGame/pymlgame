![PyMLGame Logo][pymlgame_header]

PyMLGame
========

PyMLGame is an abstraction layer to easily build games for Mate Light inspired by PyGame.

You need 3 parts to actually have a running game on Mate Light.

The game
--------

You can build a game using the PyMLGame library. If you know the PyGame library this should be nothing new to you. Use the game_example.py to find out how to do so.

A controller
------------

If you want players, your game needs a controller to have some inputs. Controllers should work with every game made with PyMLGame. There is a controller_example.py to play with. An Android based controller app is available [here][1].

Mate Light
----------

To play PyMLGames you need the awesome Mate Light. You could use the one on [c-base space station][2], or build your own. If you're not near c-base and don't want to build your own, you can use the Mate Light emulator provided with PyMLGame.


Protocol
========

This is the protocol that handles the communication between the game and the controllers. It's very similar to OSC, as it sends slash seperated srings over UDP.


Controller -> Game
------------------

### /controller/new/&lt;port&gt;

  - port: The port on the controller which the game should answer on.

Connect a new controller to the game. Game will answer with /uid/&lt;uid&gt;. This is also known as 'anpymln'.

### /controller/&lt;uid&gt;/ping/&lt;port&gt;

  - uid: The uuid given by the game to identify the controller.
  - port: The port on the controller which the game should answer on.

Tell the game that the controller is still in use and update it's address and port. Use this once every minute or the controller will be disconnected.

### /controller/&lt;uid&gt;/kthxbye

  - uid: The uuid given by the game to identify the controller.

Disconnect the controller properly. In theory you could just wait 60s but this is the cleaner way and most games would
be very happy if you use this.

###/controller/&lt;uid&gt;/states/&lt;states&gt;

  - uid: The uuid given by the game to identify the controller.
  - states: A string of 14 numbers containing the states of every button of the controller.

Send the states of your controller keys. Always send all 14 states, even if your controller doesn't have 14 buttons.
The states should be an array with 0 for key not pressed and 1 for key pressed. So if you're pressing the Up button and X button the states array should look like this: 10000010000000
You can lookup all possible buttons and there location in the array in [pymlgame/locals.py][3].

### /controller/&lt;uid&gt;/text/&lt;text&gt; *optional*

  - uid: The uuid given by the game to identify the controller.
  - text: String which should be send to the game.

Send some text to the game. Maybe it asks you for a player name or the anser to a riddle. Games should always give you the option to enter text without this function but you can use it if your controller is capable of text input.


Game -> Controller
------------------

### /uid/&lt;uid&gt;

  - uid: The uuid to identify the controller.

Tell the controller its uid. This is an UUID v4.

### /rumble/&lt;duration&gt; *optional*

  - duration: Duration in milliseconds.

Tell the controller to rumble. Remember that not all controllers have the ability to vibrate. Maybe they do it in an visual or acoustic way.

### /message/&lt;text&gt; *optional*

  - text: String to display.

Send some text to the controller. Be aware that not all controllers can display text, so don't send things that are important for the game.

### /download/&lt;url&gt; *optional*

  - url: URL to download.

Tell the controller to download the media file under the given url. The game can then ask the controller to play the
file so that the player can hear some ingame sounds. Use this function everytime the game starts because a controller
could have deleted the files after playing. Controllers should ensure that files already downloaded gets downloaded
again to reduce loading times for games that have been played before. Also games should try to have files with a unique name so that they don't get overwritten by other games. Don't call your file `sound.mp3`.

### /play/&lt;file&gt; *optional*

  - file: Filename of the media file.

Tell the controller to play the file with that name. Use the download command to download media files to the controller before using this.


Tipps
-----

If your controller downloads media files for games it is good practice to delete the downloaded stuff from time to time or give the user the ability to cleanup the downloaded files. The PyMLGame-Controller for Android will to this in a future release when you clean the apps data in the Apps view.

If your game uses some optional features, tell the players that they can have an even better gaming experience when they use a controller which is capable of these features.


---

Have fun while playing PyMLGames on Mate Light! :D

[pymlgame_header]: https://github.com/PyMLGame/pymlgame/raw/master/header.png "PyMLGame"
[1]: https://github.com/PyMLGame/pymlgame-controller
[2]: https://c-base.org/
[3]: https://github.com/PyMLGame/pymlgame/blob/master/pymlgame/locals.py
