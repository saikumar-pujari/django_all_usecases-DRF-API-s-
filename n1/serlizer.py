from rest_framework import serializers
from .models import (na, autor, book, user)


class naSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Name must be at least 3 characters long")
        return value

    class Meta:
        model = na
        fields = '__all__'


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = na
        fields = ["id", "name", ]


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = na
        fields = ["name", "email", "password"]

    def create(self, validated_data):
        return na.objects.create(**validated_data)


class authorsSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(read_only=True, many=True)
    books_count = serializers.IntegerField(
        source='books.count', read_only=True)

    class Meta:
        model = autor
        fields = '__all__'


class booksSerializer(serializers.ModelSerializer):
    # author_name = serializers.CharField(source='author.name', read_only=True)
    # str.name of the author will be shown instead of id
    # author = serializers.StringRelatedField(read_only=True)
    author = authorsSerializer()

    class Meta:
        model = book
        # fields = '__all__'
        fields = ['id', 'name', 'author']

    def create(self, validated_data):
        print(validated_data)
        author_data = validated_data.pop('author')
        print(author_data)
        author, created = autor.objects.get_or_create(**author_data)
        print(author, created)
        book_obj = book.objects.create(author=author, **validated_data)
        return book_obj


class BookSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = user
        fields = ['id', 'url', 'name']
        # extra_kwargs = {
        #     'url': {
        #         'view_name': 'hyperbaba-detail',
        #         'lookup_field': 'id'
        #     }
        # }


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'
