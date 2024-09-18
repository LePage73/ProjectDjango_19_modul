# from django.shortcuts import render # не нужна
from django.views.generic import TemplateView

# магазин компьютерных игр ####################################

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from .forms import Reg_Forms, Game_Forms
from .models import Buyer, Game, CHOICE_GENRE

# подготовим меню
MAIN_TITLE = {'title': 'Магазин компютерных игр'}
MENU = {'menu': [{'menu': 'Главная', 'href': '/game_store/'},
                 {'menu': 'Магазин', 'href': '/game_store/sale/'},
                 {'menu': 'Корзина', 'href': '/game_store/basket/'},
                 {'menu': 'Регистрация', 'href': '/game_store/signUser/'},
                 {'menu': 'Добавить игру', 'href': '/game_store/game_insert'},
                 ]}
SALE_TITLE = {'title': 'Магазин'}
BASKET_TITLE = {'title': 'Корзина'}

USER_LIST = [buy_.username.lower() for buy_ in Buyer.objects.all()]  ####################

# регистрация на сайте ######################################
class Sign_user(View):
    my_context = {}
    info = {}
    template_name = ''

    def get(self, request): # при заходе отправляем форму юзеру
        form = Reg_Forms(request.GET)
        self.info['form'] = form
        self.info['my_context'] = self.my_context
        return render(request, self.template_name, self.info)

    def post(self, request): # обработка формы
        list_err = []
        form = Reg_Forms(request.POST)
        if form.is_valid():
            if  Buyer.objects.filter(username=form.cleaned_data['username']).exists(): ################
                list_err.append('Такой пользователь существует')
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                list_err.append('Пароль и подверждение не совпадают')
            if int(form.cleaned_data['age']) < 18: list_err.append('Вам должно быть больше 18 лет')
            if len(list_err) == 0:
                Buyer.objects.create(username=form.cleaned_data['username'], age=form.cleaned_data['age'], balance=0.0)
                return render(request, '1_task/tmpl_index.html',
                              context={'user': f'Приветствуем, {form.cleaned_data['username']}!'} | {
                                  'my_context': MENU | MAIN_TITLE})
        self.info.clear()
        self.info['error'] = list_err
        self.info['form'] = form
        self.info['my_context'] = self.my_context
        return render(request, self.template_name, self.info)

    pass

Sign_user.template_name = '1_task/tmpl_sign_user.html'
Sign_user.my_context = MAIN_TITLE | MENU  # добавляем в страницу меню и заголовок

class Tmpl_store(TemplateView): # заготовка для представлений
    my_context = {}

    def get_context_data(self, *args, **kwargs, ):  # переопределим для враппинга своего контекста
        context = super().get_context_data(**kwargs)
        context['my_context'] = self.my_context
        return context

class Store_index(Tmpl_store):
    pass

Store_index.template_name = '1_task/tmpl_index.html'
Store_index.my_context = MENU | MAIN_TITLE  #  добавляем меню и заголовки в контекст

class Store_sale(Tmpl_store):

    def get_context_data(self, *args, **kwargs, ):
        self.my_context = {'cntxt_menu': [{'title': game.title,
                                           'description': game.description,
                                           'cost': game.cost,
                                           'button': 'Купить'} for game in Game.objects.all()
                                          ]} | self.my_context
        context = super().get_context_data(**kwargs)
        return context

    pass

Store_sale.template_name = '1_task/tmpl_sale.html'
Store_sale.my_context = MENU | SALE_TITLE   # добавляем меню и заголовки в контекст


class Store_basket(Tmpl_store):
    def get_context_data(self, *args, **kwargs, ):
        self.my_context = {'cntxt_menu': [{'title': game.title,
                                           'cost': game.cost,
                                           'button': 'Удалить'} for game in Game.objects.all()
                                          ]} | self.my_context
        context = super().get_context_data(**kwargs)
        return context
    pass


Store_basket.template_name = '1_task/tmpl_sale.html'
Store_basket.my_context = MENU | BASKET_TITLE # добавляем свой контекст

# добавить игру с описанием, ценой и т.д. в базу данных

class Game_Insert(View):
    my_context = {}
    info = {}
    template_name = ''

    def get(self, request):
        form_game_insert = Game_Forms(request.GET)
        self.info['form'] = form_game_insert
        self.info['my_context'] = self.my_context
        return render(request, self.template_name, self.info)

    def post(self, request):
        form_game_insert = Game_Forms(request.POST)
        if form_game_insert.is_valid():
            Game.objects.create(**form_game_insert.cleaned_data)
            return render(request, '1_task/tmpl_index.html',
                          context={'user': f'Добавлено, {form_game_insert.cleaned_data['title']}!'} | {
                              'my_context': MENU | MAIN_TITLE})
        self.info['form'] = form_game_insert
        self.info['my_context'] = self.my_context
        return render(request, self.template_name, self.info)


Game_Insert.template_name = '1_task/tmpl_game_insert.html'
Game_Insert.my_context = MENU | MAIN_TITLE