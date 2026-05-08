from n1.models import *
from django.db import connection
from pprint import pprint
from django.db.models import Case, When, Value, F


def run():
    # name, create = restruart.objects.get_or_create(
    #     name="tamil style", city="tamil")
    # print(name, create)
    # print(name.name)
    # print(name.city)
    # pprint(connection.queries)
    # pprint(name.ratings.all())
    # we can do manytomany relationship in two ways
    # name.ratings.add(rating.objects.first())
    # name.ratings.remove(rating.objects.first())
    # name.ratings.set([rating.objects.all()[:4]])
    # name.ratings.clear()

    # orders = online.objects.annotate(
    #     pagal=Case(
    #         When(no_of_item__gte=10, then=Value("high")),
    #         When(no_of_item__lt=2, then=Value("low")),
    #         When(no_of_item__gte=15, then=F("no_of_item")),
    #         default=Value("medium"),
    #         output_field=models.CharField()
    #     )
    # )
    # pprint(orders.values("stock__name", "no_of_item", "pagal"))
    # print(orders.values_list("stock__name",
    #       "no_of_item", "pagal", named=True, flat=False))
    # print(orders.values_list("stock__name", "no_of_item", "pagal", flat=False))
    # for obj in orders:
    #     print(type(obj.pagal), obj.pagal)
    # value defines the literal value to be returned

    # tasks = tasking.objects.all()
    # tasks = tasking.tasks.all()
    # tasks = tasking.tasks.pending()
    # tasks = tasking.tasks.completed()
    # print(tasks)
    # nama=pendingtasking.objects.first()
    # nama=pendingtasking.objects.last()
    # nama = pendingtasking.objects.last()
    # print(nama)
    # print(pendingtasking.objects.create(name="task 4"))
    # pprint(pendingtasking.objects.all())
    # print(pendingtasking.objects.all())
    # completedtasking.objects.create(name="task 5")
    # pprint(completedtasking.objects.all())

    # task=tasking.objects.last()
    # print(task.is_completed)
    # print(task.is_pending)