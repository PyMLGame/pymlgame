import uuid
import socket
import logging
from queue import Queue
from threading import Thread
from datetime import datetime, timedelta

from .event import Event
from .locals import *


class Controller(Thread):
    """
    A controller can be a game controller attached to the system or any other input that can trigger the controller
    functions like a smartphone app.
    """
    def __init__(self, host: str = '0.0.0.0', port: int = 1338):
        """
        Creates a controller deamon.

        :param host: Bind to address
        :param port: Bind to port
        :type host: str
        :type port: int
        """
        super().__init__()

        self.logger = logging.getLogger('controller')

        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((host, port))

        self.queue = Queue()
        # list of connected controllers
        self.controllers = {}

    def _new_controller(self, addr: str, port: int) -> uuid.UUID:
        """
        Get an id for your controller.

        :param addr: Address of the controller
        :param port: Port of the controller
        :type addr: str
        :type port: int
        :return: Unique id of the controller
        :rtype: uuid.UUID
        """
        for id, controller in self.controllers.items():
            if controller[0] == addr:
                # duplicate address. sending the id again
                self._sock.sendto(('/id/%s' % id).encode('utf-8'), (addr, port))
                return None

        # get an id and add the controller to the game
        id = uuid.uuid4().hex
        self.controllers[id] = {'addr': addr, 'port': port, 'states': '00000000000000', 'last_update': datetime.now()}

        # tell the controller about it
        self._sock.sendto(('/id/%s' % id).encode('utf-8'), (addr, port))

        # create event for pymlgame
        e = Event(id, E_NEWCTLR)
        self.queue.put_nowait(e)

        return id

    def _del_controller(self, id: str):
        """
        Remove controller from internal list and tell the game.

        :param id: Unique id of the controller
        :type id: str
        """
        try:
            self.controllers.pop(id)
            e = Event(id, E_DISCONNECT)
            self.queue.put_nowait(e)
        except KeyError:
            # There is no such controller, ignore the command
            pass

    def _ping(self, id: str, addr: str, port: int):
        """
        Just say hello so that pymlgame knows that your controller is still alive. Unused controllers will be deleted
        after a while. This function is also used to update the address and port of the controller if it has changed.

        :param id: Unique id of the controller
        :param addr: Address of the controller
        :param port: Port that the controller listens on
        :type id: str
        :type addr: str
        :type port: int
        """
        try:
            self.controllers[id]['addr'] = addr
            self.controllers[id]['port'] = port
            self.controllers[id]['last_update'] = datetime.now()

            e = Event(id, E_PING)
            self.queue.put_nowait(e)
        except KeyError:
            # There is no such controller, ignore the command
            pass

    def _update_states(self, id: str, states: str):
        """
        Got states of all buttons from a controller. Now check if something changed and create events if neccesary.

        :param id: Unique id of the controller
        :param states: Buttons states
        :type id: str
        :type states: str
        """
        # test if id exists
        if self.controllers[id]:
            # test if states have correct lenght
            if len(states) == 14:
                old_states = self.controllers[id]['states']
                if old_states != states:
                    for key in range(14):
                        if int(old_states[key]) > int(states[key]):
                            e = Event(id, E_KEYUP, key)
                            self.queue.put_nowait(e)
                        elif int(old_states[key]) < int(states[key]):
                            e = Event(id, E_KEYDOWN, key)
                            self.queue.put_nowait(e)
                self.controllers[id]['states'] = states
            self.controllers[id]['last_update'] = datetime.now()

    def _got_message(self, id: str, text):
        """
        The controller has send us a message.

        :param id: Unique id of the controller
        :param text: Text to display
        :type id: str
        :type text: str
        """
        e = Event(id, E_MESSAGE, text)
        self.queue.put_nowait(e)

        self.controllers[id]['last_update'] = datetime.now()

    def send(self, id: str, event: int, payload: str = None):
        """
        Send an event to a connected controller. Use pymlgame event type and correct payload.
        To send a message to the controller use pymlgame.E_MESSAGE event and a string as payload.

        :param id: Unique id of the controller
        :param event: Event type
        :param payload: Payload of the event
        :type id: str
        :type event: Event
        :type payload: str
        :return: Number of bytes send or False
        :rtype: int
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if id in self.controllers.keys():
            addr = self.controllers[id]['addr']
            port = self.controllers[id]['port']
            if event == E_MESSAGE:
                return sock.sendto(('/message/%s' % payload).encode('utf-8'), (addr, port))
            elif event == E_RUMBLE:
                return sock.sendto(('/rumble/%s ' % payload).encode('utf-8'), (addr, port))

        return False

    def run(self):
        """
        Listen for controllers.
        """
        while True:
            data, sender = self._sock.recvfrom(1024)
            addr, _ = sender
            try:
                msg = data.decode('utf-8').split('/')
                if msg[1] == 'controller':
                    id = msg[2]
                    if id == 'new':
                        port = int(msg[3])
                        self._new_controller(addr, port)
                    else:
                        cmd = msg[3]
                        if cmd == 'ping':
                            port = msg[4]
                            self._ping(id, addr, port)
                        elif cmd == 'kthxbye':
                            self._del_controller(id)
                        elif cmd == 'states':
                            states = msg[4]
                            self._update_states(id, states)
                        elif cmd == 'text':
                            # /controller/<uid>/text/<text>
                            text = '/'.join(msg[4:])
                            self._got_message(id, text)
            except IndexError or KeyError:
                pass

            # find unused controllers and delete them
            for id, state in self.controllers.items():
                if state['last_update'] < datetime.now() - timedelta(seconds=60):
                    self.controllers.pop(id)
