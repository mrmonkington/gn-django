from django.db import models

from gn_django.fields import UniquelyTrueBooleanField


class TestUniquelyTrueBooleanModel(models.Model):
    is_the_chosen_one = UniquelyTrueBooleanField(null=True, default=False)
