from django.urls import path

from .views import ViewHome, StudentInfoCreate, enter_code, view_pdf, pdf_page

urlpatterns = [
    path('', ViewHome.as_view(), name='home'),
    path('student/create/', StudentInfoCreate.as_view(), name='student_create'),
    path('pdf_page/<str:code>/', pdf_page, name='pdf_page'),
    path('view_pdf/<str:code>/', view_pdf, name='view_pdf'),
    path('enter-code/', enter_code, name='enter_code'),
]