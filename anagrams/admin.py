from django.contrib import admin

# Register your models here.



from .models import Anagram
from .models import Comment
from .models import Solve

admin.site.register(Anagram)
admin.site.register(Comment)
admin.site.register(Solve)