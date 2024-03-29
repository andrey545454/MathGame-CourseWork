from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(PlayerStatus)
admin.site.register(Player)
admin.site.register(Author)
admin.site.register(ProblemStatus)
admin.site.register(Problem)
admin.site.register(ProblemInGame, ProblemInGameAdmin)
admin.site.register(Game)
admin.site.register(Participation)
admin.site.register(Score)
admin.site.register(Answer)
