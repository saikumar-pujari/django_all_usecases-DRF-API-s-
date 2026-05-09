import magic
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import uuid
from django.db import models
from django.db.models import Q, F
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


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
# models.objects.values_list(flat=True)
# models.objects.count()
# models.objects.only('name')
# models.objects.defer('name')
# models.objects.exists(name="John Salas")
# models.objects.values_list('name', flat=True)
# models.objects.get(name="John Salas")
# models.objects.filter(name__icontains="john")
# models.objects.filter(book__title="Book Title")
# models.objects.with_author() #manager method
# model.objects.realted_name.all() #related name of foreign key and one to one also for reverse relation of many to many(if relatedn_name is not given then it will be modelname_set.all())
# models.objects.first()
# models.objects.last()
# models.objects.filter(id__in=[1,2,3])
# models.objects.filter(created__in__gte=datetime(2023,1,1))
# models.objects.select_related('author') #onetoine and foreign key
# models.objects.prefetch_related('author') #manytomany
# models.objects.select_for_update().get() # for locking the row in database for update and it will be released after the transaction is completed
#models.objects.raw('SELECT * FROM table_name') # for raw sql queries
#mdels.objects.bulk_create([model(name="John Salas"), model(name="Jane Doe")]) # for bulk create
#models.objects.bulk_update([model(name="John Salas", id=1), model(name="Jane Doe", id=2)], ['name']) # for bulk update

def name_should_have_styles(value):
    if 'styles' not in value:
        raise ValidationError(
            _('Name must contain the word "styles".'),
            params={'value': value},
        )


class test(models.Model):
    name = models.CharField(max_length=30, validators=[
                            name_should_have_styles])
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class restruart(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     # True if the object is being created, False if it is being updated
    #     print(self._state.adding)
    #     super().save(*args, **kwargs)


class rating(models.Model):
    restaurant = models.ForeignKey(
        restruart, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.restaurant.name} - {self.rating}"

# mutiple update
# restuart=restruart.objects.all()
# restruart.update(city="New City")


class stock(models.Model):
    name = models.CharField(max_length=30)
    stock = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)])
    comments = GenericRelation('comments', related_query_name='stocks')
    # class Meta:
    #     constraints = [
    #         # model.checkConstraint(check=Q(stock__gte=0) & Q(stock__lte=1000), name='stock_range')
    #         constraints=models.CheckConstraint(name='stock_range',check=Q(stock__gte=0) & Q(stock__lte=1000))
    #     ]

    def __str__(self):
        return f"{self.name}- {self.stock}"


class online(models.Model):
    stock = models.ForeignKey(
        stock, on_delete=models.CASCADE, related_name='online')
    no_of_item = models.PositiveSmallIntegerField()
    comments = GenericRelation('comments', related_query_name='online')

    def __str__(self):
        return f"{self.stock.name} - {self.no_of_item}"


class comments(models.Model):
    text = models.CharField(max_length=30)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={
                                         'app_label': 'n1',
                                         #  'model': ['restruart', 'stock', 'rating', 'online']
                                     }
                                     )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def clean(self):
        # model_class convert content type to model class products | n1 -> n1
        model_class = self.content_type.model_class()
        if not model_class.objects.filter(id=self.object_id).exists():
            raise ValidationError("This object_id does not exist!")

    def __str__(self):
        return self.text
# we can direclty get resturaty.objects.get(id=2) also if needed in content_object
# TabularInline in admin_panel(to add more relation between some models takes model and extra)
# stackedinline


class tasking(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    objects = models.Manager()

    class taskingmanager(models.Manager):
        def pending(self):
            return self.filter(status='pending')

        def completed(self):
            return self.filter(status='completed')
    tasks = taskingmanager()

    @property
    def is_completed(self) -> bool:
        return self.status == 'completed'

    @property
    def is_pending(self):
        return self.status == 'pending'

    # model_method
    # GeneratedField

    def __str__(self):
        return self.name


class pendingtasking(tasking):
    class Meta:
        proxy = True
        ordering = ['created_at']

    class value(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(status='pending')
    objects = value()

    def save(self, *args, **kwargs):
        self.status = 'pending'
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     self.status = 'completed'
        # self.images.delete() #when you also wanr to delete the file when object is deletd in the image then super().delete(*args, **kwargs)
    #     super().save(*args, **kwargs)


class completedtasking(tasking):
    class Meta:
        proxy = True
        ordering = ['created_at']

    class completed(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(status='completed')
    objects = completed()

    def save(self, *args, **kwargs):
        self.status = 'completed'
        super().save(*args, **kwargs)


# django.guardian
# it gives the object level permissions to the users and we can also assign the permissions to the users and groups and we can also check the permissions of the users and groups and we can also get the objects for which the user has the permission and we can also get the users who have the permission for a object and we can also get the groups who have the permission for a object
# like even thou you have many repo but you only want them to give permission to read some certain repos only!! for each user!
# from guardian.shortcuts import assign_perm, get_perms, get_objects_for_user, get_users_with_perms, get_groups_with_perms
# assign_perm('view_repo', user, repo) # to assign permission to a user for a repo
# assign_perm('view_repo', group, repo) # to assign permission to a group for a repo
# get_objects_for_user(user, 'view_repo') # to get the objects for which the user has the permission
# get_perms(user, repo) # to get the permissions of a user for a repo
# @permission_required( 'blog.delete_post',(Post, 'id', 'pk'))
# here post.id is post id number and pk is which user req(id)


# when uploading file or images use python-magic to read some content and validate the file type and also use validators in the model to validate the file type and also use clean method to validate the file type and also use signals to delete the file when the object is deleted and also use pre_save signal to delete the old file when the file is updated and also use post_save signal to delete the old file when the file is updated and also use post_delete signal to delete the file when the object is deleted



def check_file_type(file):
    file_type = magic.from_buffer(file.read(1024), mime=True,)
    print(file_type)
    if file_type not in ['image/jpeg', 'image/png', 'application/pdf']:
        raise ValidationError("Unsupported file type!")

file_type = FileExtensionValidator(['jpg', 'jpeg', 'png', 'pdf'])

class docu(models.Model):
    name = models.CharField(max_length=50)
    images = models.ImageField(
        blank=True, upload_to='images/', validators=[file_type, check_file_type])
    docu = models.FileField(
        blank=True, upload_to='documents/', validators=[file_type, check_file_type])

    def __str__(self):
        return self.name

#IMPORTANT: for the remeber me model we can just go with the AUTHENTICATIONFORM diectly and we dont need to create a custom form for it as it already has the remember me field in it and we can just use it in our login view and template and also we can use the built in login view of django and just pass the authentication form to it and also we can use the built in logout view of django and just redirect to the login page after logout and also we can use the built in password reset view of django and just pass the email template to it and also we can use the built in password reset confirm view of django and just pass the template to it and also we can use the built in password reset complete view of django and just pass the template to it


