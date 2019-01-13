from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import IntegrityError
from django.conf import settings
import os


class UserManager(BaseUserManager):
    # def create_user(self, username, email, password, is_staff, is_superuser, **kwargs):
    #     user = self.model(
    #         email=self.normalize_email(email),
    #         username=username,
    #         **kwargs
    #     )
    #
    #     user.set_password(password)
    #     user.save()
    #     return user

    def get_best(self, n_users):
        return self.order_by('-rating')[:n_users]

    # def create_superuser(self, username, email, password, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #
    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')
    #
    #     return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    upload = models.ImageField(upload_to='', verbose_name='avatar', default='default.png')
    rating = models.IntegerField(default=0, verbose_name='rating')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def image_path(self):
        if self.upload:
            return self.upload.url
        else:
            return os.path.join(settings.MEDIA_URL, "default.png")

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class TagManager(models.Manager):
    def get_best(self, n_tags):
        return self.order_by('-n_posts')[:n_tags]


class Tag(models.Model):
    title = models.CharField(max_length=200, unique=True,
                             verbose_name='tag name')
    n_posts = models.IntegerField(default=0, verbose_name='number of posts')
    objects = TagManager()

    def __str__(self):
        return self.title


class QuestionManager(models.Manager):
    def get_feed(self, order_by=None):
        order_by = order_by or ('-create_date', '-rating')
        return self.filter(is_active=True).order_by(*order_by)


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='question\'s author')

    title = models.CharField(max_length=200, verbose_name='question\'s title')
    text = models.TextField(verbose_name='question\'s text')
    create_date = models.DateTimeField(auto_now_add=True,
                                       verbose_name='created date')
    update_date = models.DateTimeField(auto_now=True,
                                       verbose_name='edit date')
    is_active = models.BooleanField(default=True, verbose_name='is active')
    tags = models.ManyToManyField(Tag, verbose_name='relevant tags')
    rating = models.IntegerField(default=0, verbose_name='question\'s rating')
    n_answers = models.IntegerField(default=0, verbose_name='number of answers')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def vote(self, user, value):
        vote = QuestionVote.objects.filter(question=self, author=user).first()
        if vote:
            vote.value = value
        else:
            vote = QuestionVote(question=self, author=user, value=value)
        vote.save()

    def get_answers(self, order_by=None):
        return self.answer_set.get_feed(order_by)

    def add_tags(self, tags):
        for tag in tags:
            if tag.pk:
                self.tags.add(tag)
            else:
                try:
                    tag.save()
                except IntegrityError:
                    t = Tag.objects.filter(title=tag.title).first()
                    self.tags.add(t)
                else:
                    self.tags.add(tag)

    def deactivate(self):
        # set is_active to false in all answers
        if not self.is_active: return self
        self.is_active = False
        for t in self.tags.all():
            t.n_posts -= 1
            t.save()
        self.author.rating -= self.rating
        self.author.save()
        self.save()
        return self

    def activate(self):
        if self.is_active: return self
        self.is_active = True
        for t in self.tags.all():
            t.n_posts += 1
            t.save()
        self.author.rating += self.rating
        self.author.save()
        self.save()
        return self

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"


class AnswerManager(models.Manager):
    def get_feed(self, order_by=None):
        order_by = order_by or ('-rating', 'create_date')
        return self.filter(is_active=True).order_by(*order_by)


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='answer\'s author')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 verbose_name='relevant question')

    text = models.TextField(verbose_name='answer\'s text')
    create_date = models.DateTimeField(auto_now_add=True,
                                       verbose_name='created date')
    update_date = models.DateTimeField(auto_now=True, verbose_name='edit date')
    is_active = models.BooleanField(default=True, verbose_name='is active')
    rating = models.IntegerField(default=0, verbose_name='answer\'s rating')

    objects = AnswerManager()

    def __str__(self):
        return f"Answer by {self.author} to q#{self.question.pk}"

    def vote(self, user, value):
        vote = AnswerVote.objects.filter(question=self,
                                         author=user).first()
        if vote is None:
            AnswerVote(question=self, author=user, value=value).save()
        else:
            vote.value = value
            vote.save()

    def deactivate(self):
        if not self.is_active: return self
        self.is_active = False
        self.question.n_answers -= 1
        self.question.save()
        self.author.rating -= self.rating
        self.author.save()
        self.save()
        return self

    def activate(self):
        if self.is_active: return self
        self.is_active = True
        self.question.n_answers += 1
        self.question.save()
        self.author.rating += self.rating
        self.author.save()
        self.save()
        return self

    class Meta:
        verbose_name = "answer"
        verbose_name_plural = "answers"


class QuestionVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='voter')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 verbose_name='voted for')
    value = models.IntegerField(verbose_name='vote value')

    class Meta:
        unique_together = ('author', 'question')

        verbose_name = "answer"
        verbose_name_plural = "answers"


class AnswerVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='voter')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,
                               verbose_name='Voted for')
    value = models.IntegerField(verbose_name='Vote value')

    class Meta:
        unique_together = ('author', 'answer')
