from django import forms
from django.forms import Field

CHOICE_GENRE = [
    ('FPS', 'Стрелялка'),
    ('RPG', 'Ролевая игра'),
    ('RTS', 'Стратегия в реальном времени'),
    ('ARC', 'Аркада'),
    ('SIM', 'Симулятор'),
    ('ADV', 'Приключения'),
]

# задаем значения полей ошибок по умолчанию
Field.default_error_messages = {'required': u'* обязательное поле', 'min_length': u'недостаточно символов'}
#######################################################################
# required - показывается, если данное поле обязательно;
# max_length - если превышено максимальное количество символов в символьном поле / в случае с файлами - длина имени файла;
# min_length - если символов меньше, чем должно быть, в символьном поле;
# invalid_choice - если выбран невозможный choice;
# invalid - при неправильном email’е и прочем неправильном вводе данных;
# max_value - если превышено числовое значение;
# min_value - если значение меньше минимального числового ограничения;
# max_digits - если превышено количество цифр в числе;
# max_decimal_places - если превышено количество цифр после запятой;
# max_whole_digits - если превышено количество цифр до запятой;
# missing - если файл не найден;
# empty - если файл пустой;
# invalid_image - если изображение повреждено;
# invalid_list  - если неправильный список choice’ов;
# invalid_link - для URLField - вызывается, если данного url не существует.

class Reg_Forms(forms.Form):
    username = forms.CharField(max_length=30, label='Ваш логин', required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Ваш пароль', required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Подтверждение пароля', required=True)
    age = forms.DecimalField(min_value=18, max_digits=3, max_value=125, decimal_places=0, label='Ваш возраст', required=True)

class Game_Forms(forms.Form):
    title = forms.CharField(max_length=100,label='Название игры', required=True)
    cost = forms.DecimalField(max_digits=7, decimal_places=2, label='Цена', required=True)
    size = forms.DecimalField(max_digits=12, decimal_places=3, label='Размер', required=True)
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    age_limited = forms.BooleanField(label='Возрастное ограничение',required=False)
    genre = forms.ChoiceField(choices=CHOICE_GENRE, label='Жанр игры', required=True)

