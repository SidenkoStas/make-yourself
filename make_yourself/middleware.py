from django.db import connection


class SQLCounterMiddleware:
    """
    Middleware that counts the amount of SQL queries made to the database.

    Parameters:
        get_response (function): The function that will be assigned to
        `self.get_response`.

    Returns:
        None
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Print amount of SQL queries
        print(f"Количество SQL-запросов: {len(connection.queries)}")
        return response
