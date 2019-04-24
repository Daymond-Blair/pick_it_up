from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create Blog Post model consisting of posts and comments.

class Post(models.Model):
    # create database fields as class attributes
    # link author to authorization user/superuser
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()  # no max length to cap blogpost
    create_date = models.DateTimeField(
        default=timezone.now(), auto_now=False, auto_now_add=False)
    published_date = models.DateTimeField(
        blank=True, null=True, auto_now=False, auto_now_add=False)  # field can be blank or null in case we don't publish or leave it off entirely

    # since published_date could be balnk or null earlier, this sets the date upon button press
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # show approved comments and hide non-approved ones
    def approve_comments(self):
        return self.comments.filter(approved_comments=True)

    # once we create a post redirect to post_detail page for the primary key "pk" of the post which was just created "self.pk"
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        "blog.Post", related_name='comments', on_delete=models.CASCADE) # connect each post to a blogpost
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(
        default=timezone.now(), auto_now=False, auto_now_add=False)
    approved_comment = models.BooleanField(default=False) # flag if a comment has been approved by setting it to false initially

    # this sets a comment to approved which will allow it to be displayed by approved_comments
    def approve(self):
        self.approved_comment = True
        self.save()

    # once we create a comment redirect back to list of posts
    def get_absolute_url(self):
        return reverse('post_list', kwargs={'pk': self.pk})

    def __str__(self):
        return self.text

    # next up, use the models to create forms
