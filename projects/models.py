from email.policy import default
from tkinter import CASCADE, FLAT
from django.db import models
import uuid
from users.models import Profile

# Create your models here. Inshort Creating our Database

class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)  # null for Database, blank for django to know blank is OKay
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=1000, null=True, blank=True)
    source_link = models.CharField(max_length=1000, null=True, blank=True)
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True) # in quotes Tag bcz Tag class is below the code, so it will give error without quotes
    created = models.DateTimeField(auto_now_add=True)  # auto_now will save every instance, but auto_now_add will save the instance when it is created
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): # string representation of the Project class
        return self.title

    class Meta:
        ordering = ['-vote_ratio', 'vote_total', 'title']

    @property
    def imageURL(self):
        try:
            img = self.featured_image.url
        except:
            img=''
        return img
    
    @property
    def reviewers(self):
        queryset = self.reviews.all().value_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.reviews.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes)*100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'up'),
        ('down', 'down')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name='reviews') 
                    # related_name helps in accessing databses, projectObj.review_set.all() part gone in views.py
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=50, choices=VOTE_TYPE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    class Meta:
        # user can review 1 review per project, so we binding this together. Also no owener can review their own project
        unique_together = [['owner', 'project']]

    def __str__(self):
        content = self.project.title + " " + self.value
        return content

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

