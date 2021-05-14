from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        first_name = reqPOST['first_name'] 
        last_name = reqPOST['last_name']
        if not first_name.isalpha() & last_name.isalpha():
            errors['letters_only'] = "First and Last name can only contain letters"
        if len(first_name) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"
        if len(last_name) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"
        if len(reqPOST['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if reqPOST['password'] != reqPOST['conf_password']:
            errors['match'] = "Password and Password Confirmation don't match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):
            errors['regex'] = "Invalid email address!"
        users_with_email = User.objects.filter(email=reqPOST['email'])
        if len(users_with_email) >=1:
            errors['dup'] = "Email taken, use another"
        return errors

class User(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = UserManager()


class Message(models.Model):
    message = models.TextField()
    posted_by = models.ForeignKey(User, related_name="messages_posted", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment = models.TextField()
    posted_by = models.ForeignKey(User, related_name="comments_posted", on_delete=models.CASCADE)
    posted_on = models.ForeignKey(Message, related_name="comments_on", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)