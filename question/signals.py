from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from question.models import Question


@receiver(pre_save, sender='question.QuestionVote',
          dispatch_uid="question_handlers_on_question_voted")
def on_question_voted(sender, instance, **kwargs):
    diff = 0
    if instance.pk:
        try:
            old_value = sender.objects.get(pk=instance.pk).value
        except sender.DoesNotExist:
            pass
        else:
            diff -= old_value
    diff += instance.value

    instance.question.rating += diff
    instance.question.author.rating += diff
    instance.question.save()
    instance.question.author.save()


@receiver(pre_save, sender='question.AnswerVote',
          dispatch_uid="question_handlers_on_answer_voted")
def on_answer_voted(sender, instance, **kwargs):
    diff = 0
    if instance.pk:
        try:
            old_value = sender.objects.get(pk=instance.pk).value
        except sender.DoesNotExist:
            pass
        else:
            diff -= old_value
    diff += instance.value

    instance.answer.rating += diff
    instance.answer.author.rating += diff
    instance.answer.save()
    instance.answer.author.save()


@receiver(post_save, sender='question.Answer',
          dispatch_uid="question_handlers_on_answer_saved")
def on_answer_saved(sender, instance, **kwargs):
    if kwargs['created']:
        instance.question.n_answers += 1
        instance.question.save()


@receiver(m2m_changed, sender=Question.tags.through,
          dispatch_uid='question_handlers_on_question_tags_changed')
def on_question_tags_changed(sender, instance, action, model, pk_set, **kwargs):
    if not instance.is_active:  # only count active questions
        return
    if action == 'pre_add':
        for tag_pk in pk_set:
            tag = model.objects.get(pk=tag_pk)
            tag.n_posts += 1
            tag.save()
    elif action == 'pre_remove':
        for tag_pk in pk_set:
            tag = model.objects.get(pk=tag_pk)
            tag.n_posts -= 1
            tag.save()
    elif action == 'pre_clear':
        for tag in instance.tags.all():
            tag.n_posts -= 1
            tag.save()
