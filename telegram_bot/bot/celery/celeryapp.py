from celery import Celery

app = Celery("myapp")

app.conf.broker_url = "redis://localhost:6379/0"
app.conf.result_backend = "redis://localhost:6379/1"

app.conf.task_queues = {
    'high': {'exchange': 'high', 'routing_key': 'high'},
    'default': {'exchange': 'default', 'routing_key': 'default'}
}

app.conf.task_routes = {
    'bot.celery.tasks.full_10_report_task': {'queue': 'high'}
}

app.conf.beat_schedule = {
    'report_every_10minutes': {
        'task': 'bot.celery.tasks.full_10_report_task',
        'schedule': 600
    }
}


