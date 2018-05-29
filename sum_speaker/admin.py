from django.contrib import admin
from .models import Candidate, Keyword, Member, Images
# Register your models here.

admin.site.register(Candidate)
admin.site.register(Keyword)
admin.site.register(Member)
admin.site.register(Images)