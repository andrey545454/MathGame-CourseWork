from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models


# Create your models here.


class PlayerStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Player statuses'


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(PlayerStatus, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class TeamStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Team statuses'


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    captain = models.ForeignKey(Player, on_delete=models.DO_NOTHING)

    players = models.ManyToManyField(Player, related_name='team_players')
    status = models.ForeignKey(TeamStatus, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Invite(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.player.user.username}-{self.team.name}'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.patronymic} {self.last_name}'


class ProblemStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Problem statuses'


class Problem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    answer = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    status = models.ForeignKey(ProblemStatus, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name


class ProblemInGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.DO_NOTHING)
    pos = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game', 'problem', 'pos'], name='unique_prob_in_game')
        ]

    def __str__(self):
        return self.problem.name


class ProblemInGameAdmin(admin.ModelAdmin):
    list_display = ('game', 'problem', 'pos')


class Participation(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    users = models.ManyToManyField(Player)

    def __str__(self):
        return str(self.id)


class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    score = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Answer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    problem = models.ForeignKey(ProblemInGame, on_delete=models.DO_NOTHING)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)
