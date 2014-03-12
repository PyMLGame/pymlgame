# pymlgame

pymlgame is an abstraction layer to easily build games for Mate Light inspired by pygame.

You need 3 parts to actually have a running game on Mate Light.

## The game

You can build a game using the pymlgame library. If you know the pygame library this should mean nothing new to you.
Use the game_example.py to find out how to do it.

## A controller

If you want players, your game needs a controller to have some inputs. You can use anything as a controller that can
speak the pymlgame controller protocol. As an example you can use the controller_example.py and adapt it to your
controller.

Here are the commands a controller can send to a pymlgame:

  - /cotroller/new
    Tell pymlgame that you want to play also known as "anpymln". It will send you a UID which should be used in
    future communication.
  - /controller/<int:uid>/ping
    Just tell pymlgame that you're still their. Also this updates your IP address so use this after a reconnect.
  - /controller/<int:uid>/kthxbye
    Be so nice and tell pymlgame that you are closing the controller on your device. That helps to avoid alot of
    garbage to go through.
  - /controller/<int:uid>/states/00000000000000
    Send the states of the 14 possible buttons. These are Up, Down, Left, Right, A, B, X, Y, Start, Select, L1, L2,
    R1, R2
  - /controller/<int:uid>/text/<str:text>
    Send a message to pymlgame. this can be used to enter player names.

These are the commands that a controller could receive:

  - /uid/<int:uid>
    Use this UID in future communication.
  - /rumble/<int:duration>
    The game wants your controller to rumble for n seconds.
  - /message/<str:text>
    The game wants your controller to display some text.

## Mate Light

Last but not least you need Mate Light as your display. If you are not at c-base space station but still want to
tinker around with this you can use the emulator.py to do so.

---

Have fun while playing pymlgames on Mate Light! :D