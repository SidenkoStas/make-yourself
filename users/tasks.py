from users.models import CustomUser
from make_yourself.celery import app
from djoser.conf import settings

mail_goal = {
    "activation": settings.EMAIL.activation,
    "confirmation": settings.EMAIL.confirmation,
    "password_reset": settings.EMAIL.password_reset,
    "password_changed_confirmation":
        settings.EMAIL.password_changed_confirmation,

}


@app.task(bind=True)
def send_email(self, context, email, purpose):
    context['user'] = CustomUser.objects.get(id=context.get('user_id'))
    try:
        mail_goal[purpose](context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
