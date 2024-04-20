from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.

def MinLengthValidator(value):
    if len(value) < 3:
        raise ValidationError(
            _("miniumum 3 letters"),
            params={"value": value},
        )

# class MinLengthValidator(limit_value, message=None)

class Anagram (models.Model):
    text = models.CharField(max_length=15, default='text', null=False, validators=[MinLengthValidator]) #difficulty based on length
    solution_text = models.CharField(max_length=15, default='solution', null=False, validators=[MinLengthValidator]) #difficulty based on length
    date_posted = models.DateField(null=True)
    solvers = models.ManyToManyField (User, through='Solve')
    #author = models.ManyToManyField(User, null=True)
    difficulty = models.CharField (max_length=20, default="medium")
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='creator')


    def __str__(self):
        return self.text

    def was_published_today(self):
        return self.date_posted >= timezone.now() - datetime.timedelta(days=1)

    def was_published_last_month(self):
        return self.date_posted >= timezone.now() - datetime.timedelta(days=30)
    
    '''
    def get_difficulty (self):
        if len(self.text) < 6 :
            difficulty = 'easy'
        elif len(self.text) > 7 :
            difficulty = 'hard'
        else:
            difficulty = 'medium'
        return difficulty
    '''

class Solve (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    anagram = models.ForeignKey(Anagram, on_delete=models.CASCADE)

    time_taken = models.IntegerField(null=True)
    solution_date = models.DateTimeField(auto_now_add=True, null=True)
    revealed = models.BooleanField(default=False)


    def last_30_days(self):
        return self.solution_date >= timezone.now() - datetime.timedelta(days=30)

    def time_length(self):
        h = self.time_taken // 3600
        r = self.time_taken-(h*3600)
        m = r // 60
        r2 = r-(m*60)
        s = r2
        if h <= 10:
            h = '0'+ str(h)
        if m <= 10:
            m = '0' + str(m)
        if s <= 10:
            s = '0' + str(s)
        number = (str(h) + ':' + str(m) + ':' + str(s))
        print (self.time_taken)

        return number
    


class Comment (models.Model):
    anagram = models.ForeignKey(Anagram, on_delete=models.CASCADE)

    text = models.CharField(max_length=60, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    date_posted = models.DateTimeField( null=True)
    likers = models.ManyToManyField(User, related_name='yes')

    def time_ago(self):
        if timezone.now()-self.date_posted > datetime.timedelta(days=2):
            number = (str(self.date_posted.day) + '/' + str(self.date_posted.month) + '/' + str(self.date_posted.year))
        '''
        elif timezone.now()-self.date_posted < datetime.timedelta(hours=1):
            number = (str((self.date_posted.second)//60)+ ' minutes ago')
        elif timezone.now()-self.date_posted < datetime.timedelta(days=1):
            number = (str((self.date_posted.second)//3600)+ ' hours ago')
        else:
            number = (str(self.date_posted.day)+ ' days ago')
            '''
        return number

    def __str__(self):
        return self.text
    
    def was_published_today(self):
        return self.date_posted >= timezone.now() - datetime.timedelta(days=1)
    
    def likes(self):
        num = self.likers.count()
        return (num)

class Reply (models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    text = models.CharField(max_length=60)

