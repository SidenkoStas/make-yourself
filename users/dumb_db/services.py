from os import path, remove
from django.conf import settings
from django.core.management import call_command
from django.http import FileResponse


class ManageDbServices:
    """
    Service for manage db.
    """
    def __init__(self, user_pk, *, file=None, target_pk=None):
        self.user_pk = user_pk
        self.file = file
        self.target_pk = target_pk

    def dump_db(self):
        """
        Dump Post db for user.
        :return: file_db.json
        """
        file_name = f"{self.user_pk}_db.json"
        file_path = path.join(
            settings.MEDIA_ROOT, file_name
        )
        # Сохраняем данные из базы данных с помощью команды dumpdata
        with open(file_path, "w") as db_dump:
            call_command("dumpdata", "blog.Post",
                         pks=self.target_pk, stdout=db_dump)

        response = FileResponse(open(file_path, "rb"))
        response['Content-Disposition'] = f"attachment; filename={file_name}"
        remove(file_path)
        return response

    def load_db(self):
        """
        Load Post db for user.
        """
        file_path = path.join(settings.MEDIA_ROOT, self.file.name)
        # Сохраняем файл на сервере
        with open(file_path, "wb+") as destination:
            for chunk in self.file.chunks():
                destination.write(chunk)

        # Загружаем данные из файла с помощью команды loaddata
        call_command("loaddata", file_path)

        remove(file_path)
