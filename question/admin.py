from django.contrib import admin

from question import models

admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.User)
admin.site.register(models.Tag)
admin.site.register(models.QuestionVote)
admin.site.register(models.AnswerVote)
