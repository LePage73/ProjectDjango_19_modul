# магазин компьютерных игр ####################################

# from django.views.generic import TemplateView

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.core.paginator import Paginator
# from django.http import HttpResponse
from .forms import Reg_Forms, Game_Forms, Game_per_Page
from .models import Buyer, Game
from .def_setting import CHOICE_GENRE, MENU, MAIN_TITLE, SALE_TITLE, BASKET_TITLE, GAME_PER_PAGE_DEF, GAME_PER_PAGE

# регистрация на сайте ######################################
class Sign_user(View):
    my_context = {}
    info = {}
    template_name = ''

    def get(self, request): # при заходе отправляем форму юзеру
        form = Reg_Forms(request.GET)
        self.info['form'] = form
        self.info['my_context'] = self.my_context
        print(request)
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
    quant_page = GAME_PER_PAGE_DEF
    info = {}
    def _paginator(self, quant_page, current_page):
        game_list = Game.objects.all().order_by('title')
        paginator = Paginator(game_list, quant_page)
        page_obj = paginator.get_page(current_page)
        elided = paginator.get_elided_page_range(on_ends=1, on_each_side=2, number=current_page)
        # создаем контекст для пажинатора
        list_elide = []
        flag_ = False
        for i in elided:
            if i == "…" and flag_ == True:  # закрывающий … - второй раз появился
                list_elide.append(">") # меняем его значение
            elif i == "…" and flag_ == False:  # открывающий … - первый раз появился
                list_elide.append("<") # меняем его значение
            elif int(i) > current_page:
                flag_ = True  # определяем открывающий или замыкающий "…"
                list_elide.append(int(i))
            else:
                list_elide.append(int(i))
                self.my_context = {'elided': list_elide,
                                   'page_number': current_page,
                                   'page_forward': current_page + 1,
                                   'page_back': current_page - 1,
                                   } | self.my_context
        return page_obj

    def get_context_data(self, *args, **kwargs, ):
        current_page = self.my_context['next_page']
        quant_page = self.my_context['quant_page']
        current_page = int(current_page)
        self.my_context = {'cntxt_menu': [{'title': game.title,
                                           'description': game.description,
                                           'genre': [v[1] for i, v in enumerate(CHOICE_GENRE) if
                                                     v[0] == game.genre].pop(),
                                           'cost': game.cost,
                                           'button': 'В корзину'} for game in
                                          self._paginator(quant_page=quant_page, current_page=current_page)
                                          ]} | self.my_context
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        form_game_per_page = Game_per_Page(request.GET)
        quant_page = self.request.GET.get('quant_page')
        next_page = self.request.GET.get('next_page')
        if quant_page is None or quant_page == 'None':
            quant_page = GAME_PER_PAGE_DEF
        if next_page is None or next_page== 'None':
            next_page = 1
        self.my_context = self.my_context | {'quant_page': int(quant_page), 'next_page': int(next_page)}
        form_game_per_page.game_p_page = int(quant_page)
        self.info['form'] = form_game_per_page
        return render(request, self.template_name, self.info | self.get_context_data(**kwargs))

    def post(self, request, **kwargs):
        form_game_per_page = Game_per_Page(request.POST)
        if form_game_per_page.is_valid():
            quant_page = form_game_per_page.cleaned_data['game_p_page']
            form_game_per_page.game_p_page = int(quant_page)
            self.info['form'] = form_game_per_page
            next_page = 1 # при смене количества игр на страницеб начинаем с 1 страницы иначе возможны ошибки в пажинаторе
            self.my_context = self.my_context | {'quant_page': int(quant_page), 'next_page': int(next_page)}
        return render(request, self.template_name, self.info | self.get_context_data(**kwargs) )
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
        form_game_insert = Game_Forms(request.GET, initial={'title':'Название игры', 'cost': 99.5})
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