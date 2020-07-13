from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('doctors', views.all_doctors, name="doctors"),
    path('departments', views.all_departments, name="departments"),
    path('department/<name>', views.per_department, name="department"),
    path('doctor/<id>', views.per_doct, name="doctor"),
    path('myProfile', views.myProfile, name="myProfile"),
    path('profile/<id>', views.profile, name="profile"),
    path('send_request', views.send_request, name="send_request"),
    path('reject/<id>', views.reject, name="reject"),
    path('completed/<id>', views.completed, name="completed")

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
