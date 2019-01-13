from django.db import IntegrityError
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormView, ModelFormMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from question.models import Question, Tag, User, Answer, \
    QuestionVote, AnswerVote
from question.forms import SignupForm, QuestionCreateForm, \
    ProfileEditForm, AnswerForm


class QuestionMandatoryMixin(ContextMixin):
    active_top_link = None
    request = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_name'] = 'Askme'
        context['top_links'] = [
            {'title': 'Home',
             'url': reverse('question:index-view'),
             'active': self.active_top_link == 'home'},
            {'title': 'Hot',
             'url': reverse('question:hot-view'),
             'active': self.active_top_link == 'hot'},
        ]
        if self.request.user.is_authenticated:
            context['top_links'].append({'title': 'Ask a Question',
                                         'url': reverse('question:new-question-view'),
                                         'active': self.active_top_link == 'new_question'})
        else:
            context['top_links'].append({'title': 'Sign Up',
                                         'url': reverse('question:signup'),
                                         'active': self.active_top_link == 'sign_up'})
        return context


class QuestionRightBlockMixin(QuestionMandatoryMixin):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['base'] = {
            'top_tags': Tag.objects.get_best(5),
            'top_users': User.objects.get_best(5)
        }
        return context


class IndexView(ListView, QuestionRightBlockMixin):  # order is important
    model = Question
    template_name = 'question/index.html'
    paginate_by = 10
    context_object_name = 'questions'
    active_top_link = 'home'

    def get_queryset(self, **kwargs):
        return Question.objects.get_feed()


class HotView(IndexView):
    active_top_link = 'hot'

    def get_queryset(self, **kwargs):
        return Question.objects.get_feed(order_by=('-rating', 'create_date'))


class QuestionView(ListView, QuestionRightBlockMixin):
    model = Answer
    template_name = 'question/question_detail.html'
    question = None
    paginate_by = 3
    context_object_name = 'answers'

    def dispatch(self, request, *args, **kwargs):
        question_pk = self.kwargs['pk']
        self.question = Question.objects.filter(pk=question_pk).first()
        if self.question is None:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.question.get_answers()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'question': self.question
        })
        return context

    def post(self, request, *args, **kwargs):
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            a = Answer(author=request.user, question=self.question,
                       text=form.cleaned_data['text'])
            a.save()
            return JsonResponse({'status': 'OK',
                                 'success_url': reverse('question:question-view',
                                                        args=[kwargs['pk']])})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


class TagView(ListView, QuestionRightBlockMixin):
    model = Question
    template_name = 'question/tag_detail.html'
    tag = None
    paginate_by = 10
    context_object_name = 'questions'

    def dispatch(self, request, *args, **kwargs):
        tag_pk = self.kwargs['pk']
        self.tag = Tag.objects.filter(pk=tag_pk).first()
        if self.tag is None:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        return Question.objects.get_feed().filter(tags=self.tag)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'tag': self.tag
        })
        return context


class ProfileView(DetailView, QuestionMandatoryMixin):
    model = User
    template_name = 'question/user_detail.html'
    form_class = ProfileEditForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        questions = self.object.question_set.get_feed(
            order_by=('-rating', '-create_date')).filter(rating__gt=0)[:5]
        answers = self.object.answer_set.get_feed().filter(rating__gt=0)[:5]
        context['questions'] = questions
        context['answers'] = answers
        return context


class ProfileEditView(ModelFormMixin, DetailView, QuestionMandatoryMixin):
    model = User
    template_name = 'question/user_edit.html'
    form_class = ProfileEditForm
    object = None

    def get_success_url(self):
        return reverse('question:profile-view', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = User.objects.filter(pk=kwargs.get('pk')).first()
        if self.object is None:
            raise Http404
        if request.user.pk != self.object and not request.user.is_superuser:
            raise PermissionDenied
        form = ProfileEditForm(data=request.POST,
                               files=request.FILES,
                               instance=self.object)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'OK',
                                 'success_url': reverse('question:profile-view',
                                                        args=[kwargs['pk']])})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


class QuestionCreateView(TemplateView, QuestionRightBlockMixin):
    template_name = 'question/question_create.html'
    form_class = QuestionCreateForm
    active_top_link = 'new_question'

    @method_decorator(login_required)
    def post(self, request):
        form = QuestionCreateForm(data=request.POST)
        if form.is_valid():
            q = form.save(author=request.user)
            return JsonResponse({'status': 'OK',
                                 'success_url': reverse('question:question-view',
                                                        args=[q.pk])})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


class QuestionCreateAjaxView(View):
    http_method_names = ['post']


class SignupView(FormView, QuestionRightBlockMixin):
    template_name = 'question/signup.html'
    form_class = SignupForm
    success_url = ''
    active_top_link = 'sign_up'

    def form_valid(self, form):
        return super().form_valid(form)


class SignupAjaxView(View):
    http_method_names = ['post']

    def post(self, request):
        form = SignupForm(data=request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
            return JsonResponse({'status': 'OK', 'success_url': ''})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


class LoginAjaxView(View):
    http_method_names = ['post']

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            # username = form.cleaned_data.get('login_username')
            username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('login_password')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'status': 'OK', 'success_url': ''})
            return JsonResponse({'status': 'ERROR', 'errors': ['Пользователь не найден.']})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


class LogoutAjaxView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({'status': 'OK', 'success_url': ''})


class QuestionUpvoteAjaxView(View):
    http_method_names = ['post']

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return {'status': 'ERROR', 'message': 'Not logged in.'}

        fields = {
            'question': Question.objects.filter(pk=kwargs.get('pk')).first(),
            'author': User.objects.filter(pk=request.user.pk).first(),
            'value': 1,
        }

        try:
            qv = QuestionVote(**fields)
            qv.save()
        except IntegrityError:
            return JsonResponse({'status': 'ERROR', 'message': 'Vote is already present.'})
        return JsonResponse({'status': 'OK'})


class QuestionDownvoteAjaxView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return {'status': 'ERROR', 'message': 'Not logged in.'}

        fields = {
            'question': Question.objects.filter(pk=kwargs.get('pk')).first(),
            'author': User.objects.filter(pk=request.user.pk).first(),
            'value': -1,
        }

        try:
            qv = QuestionVote(**fields)
            qv.save()
        except IntegrityError:
            return JsonResponse({'status': 'ERROR', 'message': 'Vote is already present.'})
        return JsonResponse({'status': 'OK'})


class AnswerUpvoteAjaxView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return {'status': 'ERROR', 'message': 'Not logged in.'}

        fields = {
            'answer': Answer.objects.filter(pk=kwargs.get('pk')).first(),
            'author': User.objects.filter(pk=request.user.pk).first(),
            'value': 1,
        }

        try:
            av = AnswerVote(**fields)
            av.save()
        except IntegrityError:
            return JsonResponse({'status': 'ERROR', 'message': 'Vote is already present.'})
        return JsonResponse({'status': 'OK'})


class AnswerDownvoteAjaxView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return {'status': 'ERROR', 'message': 'Not logged in.'}

        fields = {
            'answer': Answer.objects.filter(pk=kwargs.get('pk')).first(),
            'author': User.objects.filter(pk=request.user.pk).first(),
            'value': -1,
        }

        try:
            av = AnswerVote(**fields)
            av.save()
        except IntegrityError:
            return JsonResponse({'status': 'ERROR', 'message': 'Vote is already present.'})
        return JsonResponse({'status': 'OK'})
