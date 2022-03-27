from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class PlayerStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Player statuses'


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    status = models.OneToOneField(PlayerStatus, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user.id}. {self.user.first_name} {self.user.last_name}'


class TeamStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Team statuses'


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    players = models.ManyToManyField(Player)
    status = models.OneToOneField(TeamStatus, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.id}. {self.name}'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.patronymic} {self.last_name}'


class ProblemStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        verbose_name_plural = 'Problem statuses'


class Problem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    answer = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    status = models.OneToOneField(ProblemStatus, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class ProblemInGame(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.DO_NOTHING)
    pos = models.IntegerField()

    def __str__(self):
        return self.problem.name


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    problems = models.ManyToManyField(ProblemInGame)

    def __str__(self):
        return self.name


class Participation(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    users = models.ManyToManyField(Player)

    def __str__(self):
        return self.id


class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    score = models.IntegerField()

    def __str__(self):
        return self.id


class Answer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    problem = models.ForeignKey(ProblemInGame, on_delete=models.DO_NOTHING)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.id
