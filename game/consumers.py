import re
import logging
from channels import Group
from channels.sessions import channel_session
from .models import Game, GameSquare
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
log = logging.getLogger(__name__)
from django.utils.decorators import method_decorator

from channels.generic.websockets import JsonWebsocketConsumer


class LobbyConsumer(JsonWebsocketConsumer):

    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True


    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        print("adding to connection group lobby")
        return ["lobby"]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        pass

    def receive(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        channel_session_user = True

        action = content['action']
        if action == 'create_game':
            # create a new game using the part of the channel name
            Game.create_new(self.message.user)

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass


class GameConsumer(JsonWebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["game-{0}".format(kwargs['game_id'])]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        pass

    def receive(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        channel_session_user = True
        action = content['action']
        print("MESSAGE ON OBSTRUCTION - {0}".format(action))

        if action == 'claim_square':
            # get the square object
            square = GameSquare.get_by_id(content['square_id'])
            square.claim('Selected', self.message.user)

        if action == 'chat_text_entered':
            # chat text
            game = Game.get_by_id(content['game_id'])
            game.add_log(content['text'], self.message.user)
            game.send_game_update()

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass




