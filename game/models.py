from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from channels import Group
import json
from datetime import datetime


class Game(models.Model):
    winner = models.ForeignKey(
        User, related_name='winner', null=True, blank=True)
    creator = models.ForeignKey(User, related_name='creator')
    opponent = models.ForeignKey(
        User, related_name='opponent', null=True, blank=True)
    cols = models.IntegerField(default=6)
    rows = models.IntegerField(default=6)
    current_turn = models.ForeignKey(User, related_name='current_turn')

    # dates
    completed = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Game #{0}'.format(self.pk)

    @staticmethod
    def get_available_games():
        return Game.objects.filter(opponent=None, completed=None)

    @staticmethod
    def created_count(user):
        return Game.objects.filter(creator=user).count()

    @staticmethod
    def get_games_for_player(user):
        from django.db.models import Q
        return Game.objects.filter(Q(opponent=user) | Q(creator=user))

    @staticmethod
    def get_by_id(id):
        try:
            return Game.objects.get(pk=id)
        except Game.DoesNotExist:
            # TODO: Handle this Exception
            pass

    @staticmethod
    def create_new(user):
        """
        Create a new game and game squares
        :param user: the user that created the game
        :return: a new game object
        """
        # make the game's name from the username and the number of
        # games they've created
        new_game = Game(creator=user, current_turn=user)
        new_game.save()
        # for each row, create the proper number of cells based on rows
        for row in range(new_game.rows):
            for col in range(new_game.cols):
                new_square = GameSquare(
                    game=new_game,
                    row=row,
                    col=col
                )
                new_square.save()
        # put first log into the GameLog
        new_game.add_log('Game created by {0}'.format(new_game.creator.username))

        return new_game

    def add_log(self, text, user=None):
        """
        Adds a text log associated with this game.
        """
        entry = GameLog(game=self, text=text, player=user).save()
        return entry

    def get_all_game_squares(self):
        """
        Gets all of the squares for this Game
        """
        return GameSquare.objects.filter(game=self)

    def get_game_square(row, col):
        """
        Gets a square for a game by it's row and col pos
        """
        try:
            return GameSquare.objects.get(game=self, cols=col, rows=row)
        except GameSquare.DoesNotExist:
            return None

    def get_square_by_coords(self, coords):
        """
        Retrieves the cell based on it's (x,y) or (row, col)
        """
        try:
            square = GameSquare.objects.get(row=coords[1],
                                            col=coords[0],
                                            game=self)
            return square
        except GameSquare.DoesNotExist:
            # TODO: Handle exception for gamesquare
            return None

    def get_game_log(self):
        """
        Gets the entire log for the game
        """
        return GameLog.objects.filter(game=self)

    def send_game_update(self):
        """
        Send the updated game information and squares to the game's channel group
        """
        # imported here to avoid circular import
        from serializers import GameSquareSerializer, GameLogSerializer, GameSerializer

        squares = self.get_all_game_squares()
        square_serializer = GameSquareSerializer(squares, many=True)

        # get game log
        log = self.get_game_log()
        log_serializer = GameLogSerializer(log, many=True)

        game_serilizer = GameSerializer(self)

        message = {'game': game_serilizer.data,
                   'log': log_serializer.data,
                   'squares': square_serializer.data}

        game_group = 'game-{0}'.format(self.id)
        Group(game_group).send({'text': json.dumps(message)})

    def next_player_turn(self):
        """
        Sets the next player's turn
        """
        self.current_turn = self.creator if self.current_turn != self.creator else self.opponent
        self.save()

    def mark_complete(self, winner):
        """
        Sets a game to completed status and records the winner
        """
        self.winner = winner
        self.completed = datetime.now()
        self.save()


class GameSquare(models.Model):
    STATUS_TYPES = (
        ('Free', 'Free'),
        ('Selected', 'Selected'),
        ('Surrounding', 'Surrounding')
    )
    game = models.ForeignKey(Game)
    owner = models.ForeignKey(User, null=True, blank=True)
    status = models.CharField(choices=STATUS_TYPES,
                              max_length=25,
                              default='Free')
    row = models.IntegerField()
    col = models.IntegerField()

    # dates
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0} - ({1}, {2})'.format(self.game, self.col, self.row)

    @staticmethod
    def get_by_id(id):
        try:
            return GameSquare.objects.get(pk=id)
        except GameSquare.DoesNotExist:
            # TODO: Handle exception for gamesquare
            return None

    def get_surrounding(self):
        """
        Returns this square's surrounding neighbors that are still Free
        """
        # TODO:
        # http://stackoverflow.com/questions/2373306/pythonic-and-efficient-way-of-finding-adjacent-cells-in-grid
        ajecency_matrix = [(i, j) for i in (-1, 0, 1)
                           for j in (-1, 0, 1) if not (i == j == 0)]
        results = []
        for dx, dy in ajecency_matrix:
            # boundaries check
            if 0 <= (self.col + dy) < self.game.cols and 0 <= self.row + dx < self.game.rows:
                # yield grid[x_coord + dx, y_coord + dy]
                results.append((self.col + dy, self.row + dx))
        return results

    def claim(self, status_type, user):
        """
        Claims the square for the user
        """
        self.owner = user
        self.status = status_type
        self.save(update_fields=['status', 'owner'])

        # get surrounding squares and update them if they can be updated
        surrounding = self.get_surrounding()

        for coords in surrounding:
            # get square by coords
            square = self.game.get_square_by_coords(coords)

            if square and square.status == 'Free':
                square.status = 'Surrounding'
                square.owner = user
                square.save()

        # add log entry for move
        self.game.add_log('Square claimed at ({0}, {1}) by {2}'
                          .format(self.col, self.row, self.owner.username))

        # set the current turn for the other player if there are still free
        # squares to claim
        if self.game.get_all_game_squares().filter(status='Free'):
            self.game.next_player_turn()
        else:
            self.game.mark_complete(winner=user)
        # let the game know about the move and results
        self.game.send_game_update()


class GameLog(models.Model):
    game = models.ForeignKey(Game)
    text = models.CharField(max_length=300)
    player = models.ForeignKey(User, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Game #{0} Log'.format(self.game.id)


