from django.db import models


class SocialNetwork(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    topic = models.TextField()

    def __str__(self):
        return self.topic


class User(models.Model):
    user_id = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, null=False)
    friends = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Post(models.Model):
    post_id = models.CharField(max_length=250, primary_key=True)
    text = models.TextField()
    shares = models.IntegerField(default=0)
    create_date = models.DateField(null=False)
    favorite = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)
    language = models.CharField(max_length=25, default='es', null=False)

    def __str__(self):
        return self.text
