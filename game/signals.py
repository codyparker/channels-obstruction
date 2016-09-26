from django.db.models.signals import post_save
from django.dispatch import receiver
from game.models import *
import json
from channels import Group
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .serializers import *
from .models import Game, GameSquare, GameLog


@receiver(post_save, sender=Game)
def new_game_handler(**kwargs):
    """
    When a new game is created, this builds a list of all open games and 
    sends it down to all channels in the 'lobby' group
    """
    # if new
    if kwargs['created']:
        # send the latest list to all channels in the "lobby" group
        # the Group's send method requires a dict
        # we pass "text" as the key and then serialize the list of open games
        avail_game_list = Game.get_available_games()
        avail_serializer = GameSerializer(avail_game_list, many=True)
        Group('lobby').send({'text': json.dumps(avail_serializer.data)})
