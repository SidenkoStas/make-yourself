from djoser.compat import get_user_email


def get_email_context(user, request):
    context = {
        'user_id': user.id,
        'domain': request.get_host(),
        'protocol': 'https' if request.is_secure() else 'http',
        'site_name': request.get_host()
    }
    email = [get_user_email(user)]
    return context, email
