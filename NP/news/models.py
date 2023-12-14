from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Author(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = \
            sum(x * 3 for x in range(Post.filter(author=self).values(rating))) + \
            sum(x for x in range(Comment.user.filter(author=self).values(rating))) + \
            sum(x for x in range(Comment.post.filter(author=self).values(rating)))


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    article = 'ARTICLE'
    news = 'NEWS'
    TYPE_CHOICES = (
        (article, 'Article'),
        (news, 'News')
    )
    type = models.CharField(
        max_length=7, choices=TYPE_CHOICES, default='article')
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    tittle = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        return self.rating

    def dislike(self):
        self.rating -= 1
        return self.rating

    def preview(self):
        return self.text[:128] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        return self.rating

    def dislike(self):
        self.rating -= 1
        return self.rating
