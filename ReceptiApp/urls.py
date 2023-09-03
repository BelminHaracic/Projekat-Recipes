from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    path('registration', views.registration, name="registration"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('delete_acc', views.delete_acc, name="delete_acc"),
    path('preporuka_recepta', views.preporuka_recepta, name="preporuka_recepta"),
    path('pretraga_recepata', views.pretraga_recepata, name="pretraga_recepata"),
    path('kontakt', views.kontakt, name="kontakt"),
    path('autori', views.autori, name="autori"),
    path('komentari', views.autori, name="komentari"),
    path('prikazi_recept/<int:recept_id>', views.prikazi_recept, name="prikazi_recept"),
    path('izbrisi_komentar/<int:komentar_id>', views.izbrisi_komentar, name="izbrisi_komentar"),
    path('edit_komentar/<int:komentar_id>', views.edit_komentar, name="edit_komentar"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +\
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
