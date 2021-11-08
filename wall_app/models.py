from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        if len(postdata['first_name']) < 2:
            errors['first_name'] = "First name must be at least two characters long"
        if len(postdata['last_name']) < 2:
            errors['first_name'] = "Last name must be at least two characters long"
        
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postdata['email'])== 0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postdata['email']):
            errors['email'] = "Must be a valid email"
        
        current_users = User.objects.filter(email = postdata['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email is already in use"

        if len(postdata['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postdata['password'] != postdata['confirm_password']:
            errors['mismatch'] = "Your passwords do not match"
        return errors
        

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    objects = UserManager()

class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="post_comments", on_delete=models.CASCADE)
