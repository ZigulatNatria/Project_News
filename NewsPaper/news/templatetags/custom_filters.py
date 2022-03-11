from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    curse_word = ['мат', 'ещёмат', 'многомата']  # список матерных слов
    for i in range(len(curse_word)):
        value = value.replace(curse_word[i], '***') # подставляем в заменяемое значение матерное слово из списка и перезаписываем переменную
    return value



