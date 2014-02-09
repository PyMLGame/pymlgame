# pymlgame

pymlgame is an abstraction layer to easily build games for Mate Light inspired
by pygame.

You need 3 parts to actually have a running game on Mate Light.

## The game

You can build a game using the pymlgame library. If you know the pygame
library this should meen nothing new to you. Use the game_example.py to find
out how to to so.

## A controller

If you want players, your game needs a controller to have some inputs. You
can use anything as a controller that can trigger the JSONRPC calls in your
game. As an example you can use the controller_example.py and adapt it to
your controller.

## Mate Light

Last but not least you need Mate Light as your display. If you are not at
c-base space station but still want to tinker around with this you can use
the emulator.py to do so.

---

Have fun while playing pymlgames on Mate Light! :D