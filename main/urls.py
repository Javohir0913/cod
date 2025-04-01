from django.urls import path

from .views import ViewHome, StudentInfoCreate, enter_code

urlpatterns = [
    path('', ViewHome.as_view(), name='home'),
    path('student/create/', StudentInfoCreate.as_view(), name='student_create'),
    path('enter-code/', enter_code, name='enter_code'),
]