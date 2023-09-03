from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(MyUser)
admin.site.register(Sastojak)
admin.site.register(Recept)
admin.site.register(SastojakRecept)
admin.site.register(Komentar)
admin.site.register(Kontakt)


