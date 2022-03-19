from django_filters import FilterSet
from .models import Post
import django_filters
import django.forms

class PostFilter(FilterSet): #Определяем фильтр
    date = django_filters.DateFilter(
    field_name="dateCreation",    #Имя поля по которому фильтруем
    lookup_expr="gt",
    label="Дата от",           #Подпись поля для отображения
    widget=django.forms.DateInput(     #Виджет
                    attrs={
                        'type': 'date'
                    })
    )

    date.field.error_messages = {'invalid': 'Введите дату в формате ДД.ММ.ГГГГ. Например 05.07.1988'} #Сообщение при ошибке
    date.field.widget.attrs = {'placeholder': 'ДД.ММ.ГГГГ'}    #Подсказа по вводу даты


    class Meta:
        model = Post #Наименование модели по которой работает фильтрация
        fields = {
                'title': ['icontains'],  #Поля для фильтрации
                'author': ['exact'],
                }   # указываем наименования полей по которым будет работать фильтр





