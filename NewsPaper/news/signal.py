from django.dispatch import receiver
from .models import PostCategory, Category, Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save


@receiver(post_save, sender= PostCategory)
def new_post_created(sender, instance, created, **kwargs):
    if created:
        category_name = instance.categoryTrough
        title = Post.objects.get(id= instance.postTrough.id).title
        text = Post.objects.get(id= instance.postTrough.id).text
        qs = Category.objects.filter(name=category_name).values('subscribe__username', 'subscribe__email')
        for object in qs:
            subscriber_username = object.get('subscribe__username')

        # получаем наш html
        html_content = render_to_string(
            'letter.html',
            {
                'subscriber_username': subscriber_username,
                'title': title,
                'category_name': category_name,
                'text': text,
                'post': Post.objects.get(id=instance.postTrough.id)
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=title,
            body=f'{text}, {category_name}',  # это то же, что и message
            from_email='vachrameev.oleg@yandex.ru',
            to=[object.get('subscribe__email')],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем