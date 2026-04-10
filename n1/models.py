import uuid
from django.db import models
from django.db.models import Q, F
from django.utils.translation import gettext_lazy as _


class data(models.Model):
    name = models.CharField(_("testing name"), max_length=50)


class usser(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class postmanager(models.Manager):
    def get_queryset(self):
        return postqueryset(self.model, using=self._db)

    def published(self) -> models.QuerySet:
        # return self.filter(status='published')
        return self.get_queryset().published()

    def popular(self) -> models.QuerySet:
        return self.filter(views__gt=100)


class postqueryset(models.QuerySet):
    def published(self) -> models.QuerySet:
        return self.filter(status='published')

    def popular(self) -> models.QuerySet:
        return self.filter(views__gt=100)

    def by_author(self, name) -> models.QuerySet:
        return self.filter(author__name=name)

    def by_title(self, title) -> models.QuerySet:
        return self.filter(Q(title="Django") | Q(title="Python"))

    def increase_views(self, id):
        return self.filter(id=id).update(views=models.F('views') + 10)


class post(models.Model):
    title = models.CharField(max_length=100, editable=False)
    content = models.TextField()
    status = models.CharField(
        choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    views = models.IntegerField(default=0)
    author = models.ForeignKey('user', on_delete=models.CASCADE)

    objects = postmanager()
    objects = postqueryset.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Post_all'
        managed = True
        ordering = ['-views', 'title']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        # unique_together = ['title', 'author'] #old way of doing unique together
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'], name='unique_title_author')]
        indexes = [models.Index(fields=['title', 'author']),
                   models.Index(fields=['status'])]
        # Permissions = [('can_publish', 'Can publish post')]


class time(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class na(time):
    name = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return self.name

    class Meta(time.Meta):
        db_table = 'na_all'
        managed = True  # will createand manage the table in DB if true
        ordering = ['name']


class ba(time):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta(time.Meta):
        db_table = 'ba_all'
        managed = True  # will createand manage the table in DB if true
        ordering = ['name']


# class proxyuser(post):
#     class Meta:
#         proxy = True
#         ordering = ['name']

class basemodel(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

    class Meta:
        abstract = True


class com1(basemodel):
    pincode = models.IntegerField()


class com2(basemodel):
    age = models.IntegerField()
    city = None


class autor(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class book(models.Model):
    name = models.CharField(max_length=30)
    author = models.ForeignKey(
        autor, on_delete=models.CASCADE, related_name='books')
    # using related name we can access the books of an author by author.books.all() else we have to do book.objects.filter(author=author) which is less efficient its like reverse relation and we can also do author.books.count() to get the count of books of an author
    # f=names.objects.all(),s=f.get(name="John Salas"),s.namesproxy
    # namesproxy.objects.filter(name__name="John Salas")

    def __str__(self) -> str:
        return self.name


class user(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# in one to one we dont use .all() as it has only object we use .first() also we can use foreign related_name code here like author.profile or safeway is hasattr(author,'profile'),hasattr(s,"namesproxy")


class Profile(models.Model):
    user = models.OneToOneField(
        user,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    bio = models.TextField()


class ProfileProtect(models.Model):
    user = models.OneToOneField(
        user,
        on_delete=models.PROTECT,
        related_name="profile_protect"
    )


class ProfileNull(models.Model):
    user = models.OneToOneField(
        user,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile_null"
    )


def get_default_user():
    return user.objects.first().id if user.objects.exists() else None


class ProfileDefault(models.Model):
    user = models.OneToOneField(
        user,
        on_delete=models.SET_DEFAULT,
        default=get_default_user,
        related_name="profile_default"
    )


class ProfileRestrict(models.Model):
    user = models.OneToOneField(
        user,
        on_delete=models.RESTRICT,
        related_name="profile_restrict"
    )


class names(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class namesproxy(models.Model):
    name = models.OneToOneField(
        names, on_delete=models.CASCADE, related_name='namesproxy')
    # onetoone can be accesed using .all() .first() .last() just the names like namesproxy.objects.filter(name__name="John Salas").first() or namesproxy.objects.filter(name__name="John Salas").last() or namesproxy.objects.filter(name__name="John Salas").all() but it will return only one object as its onetoone relation and we can also access the namesproxy of a name using name.namesproxy and we can also check if a name has a namesproxy using hasattr(name,'namesproxy') and we can also check if a namesproxy has a name using hasattr(namesproxy,'name')

# also select_related is used to optimize the queries in foreign key and one to one relationships and prefetch_related is used to optimize the queries in many to many relationships
# 1 SINGLE query → fetch books + authors together (JOIN) related

# authors = Author.objects.prefetch_related("books")
# for a in authors:
#     print(a.name, list(a.books.all()))

# books = Book.objects.select_related("author")
# for b in books:
#     print(b.title, b.author.name)


class uuidmodel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class uuidsmodel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class images(models.Model):
    name = models.CharField(max_length=50)
    images = models.ImageField(blank=True, upload_to='images/')
    docu = models.FileField(blank=True, upload_to='documents/')

    def __str__(self):
        return self.name

# ORM code for all the models!
# models.objects.create(name="John Salas", city="New York")
# models.objects.filter(name="John Salas")
# models.objects.exclude(name="John Salas")
# models.objects.filter(name="John Salas").update(city="Los Angeles")
# models.objects.filter(name="John Salas").delete()
# models.objects.filter(Q(name="John Salas") | Q(city="New York")) #|, & , ~
# models.objects.filter(update=F('views')+10)
# models.objects.all()
# models.objects.all().distinct()
# models.objects.order_by('name')
# models.objects.values()
# models.objects.count()
# models.objects.only('name')
# models.objects.defer('name')
# models.objects.exists(name="John Salas")
# models.objects.values_list('name', flat=True)
# models.objects.get(name="John Salas")
# models.objects.filter(name__icontains="john")
# models.objects.filter(book__title="Book Title")
# models.objects.with_author() #manager method
# models.objects.first()
# models.objects.last()
# models.objects.filter(id__in=[1,2,3])
# models.objects.filter(created__in__gte=datetime(2023,1,1))
# models.objects.select_related('author') #onetoine and foreign key
# models.objects.prefetch_related('author') #manytomany


class test(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.name
