from game.models import *
from django.contrib.auth.models import User


def clearSquares():
    user = User.objects.get(pk=2)
    GameSquare.objects.all().update(owner=None, status="Free")
    Game.objects.filter(pk=6).update(current_turn=user, completed=None)
    GameLog.objects.filter(game__id=6).delete()


def clearAll():
    Game.objects.all().delete()
    GameSquare.objects.all().delete()
    GameLog.objects.all().delete()
