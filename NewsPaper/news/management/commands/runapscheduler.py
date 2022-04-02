import logging

from ...models import *

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def periodic_subscribers_mailing():
    category_set = Category.objects.all().values('name')
    categories_list = []

    for _category in category_set:
        categories_list.append(_category.get('name'))

    for category in categories_list:
        category_id = Category.objects.get(name=category).id

        posts_qs = Post.objects.order_by('-dateCreation').filter(postCategory=category_id).values('id', 'title')[0:10]

        cat_qs = Category.objects.filter(name=category).values('subscribers__username', 'subscribers__email')

        for subs in cat_qs:
            subscriber_username = subs.get('subscribe__username')
            subscriber_email = subs.get('subscribe__email')

            html_content = render_to_string(
                'news_updated_weekly.html',
                {
                    'subscriber_username': subscriber_username,
                    'posts_qs': posts_qs,
                    'category': category
                }
            )
            msg = EmailMultiAlternatives(
                subject=f"Последние",
                body=f"Здравствуй, {subscriber_username}. Последние новости...",
                from_email='vachrameev.oleg@yandex.ru',
                to=[subscriber_email],
            )

            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем
            print("Отправлено")


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            periodic_subscribers_mailing,
            trigger=CronTrigger(second="*/1"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="periodic_subscribers_mailing",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'periodic_subscribers_mailing'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=10,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
