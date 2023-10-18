from tortoise import fields
from tortoise.models import Model


class Student(Model):
    user_tg_id = fields.IntField(pk=True)
    guid = fields.CharField(max_length=255)

    class Meta:
        table = "student"

    def __str__(self):
        return self.guid
