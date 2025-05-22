
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.http import JsonResponse
from django.shortcuts import render
import os
from django.http import FileResponse, Http404

from .models import StudentInfo

# Create your views here.
class StudentInfoCreate(CreateView):
    model = StudentInfo
    fields = ('student_file',)  # Faqat 'student_file' maydoni
    template_name = 'student_info_crate.html'
    success_url = reverse_lazy('student_create')

    def form_valid(self, form):
        # Faylni saqlashdan oldin nomini o'zgartirish
        file = form.cleaned_data['student_file']
        # Fayl nomini olish
        file_name = file.name

        # Faylning kengaytmasini olib tashlash
        file_name_without_extension, file_extension = os.path.splitext(file_name)

        # Agar fayl .pdf kengaytmaga ega bo'lsa
        if file_extension == '.pdf':
            # Yangi fayl nomi va ID saqlash
            form.instance.file_id = file_name_without_extension  # file_id uchun nomni saqlash
            return super().form_valid(form)

        # Agar kengaytma mos kelmasa, xatolikni qaytarish
        form.add_error('student_file', 'Fayl faqat .pdf bo\'lishi kerak')
        return super().form_invalid(form)


class ViewHome(TemplateView):
    template_name = 'main.html'


def enter_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        try:
            student_info = StudentInfo.objects.get(file_id=code)
            print(student_info)
            file_path = student_info.student_file.path  # Fayl manzili

            # Faylni tekshirish
            if os.path.exists(file_path):
                return JsonResponse({
                    'status': 'success',
                    'file_url': student_info.student_file.url  # Fayl URL'ini yuborish
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Fayl topilmadi'
                })

        except StudentInfo.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Неверный код'
            })

    return render(request, 'enter_code.html')

def view_pdf(request, code):
    try:
        student_info = StudentInfo.objects.get(file_id=code)
        file_path = student_info.student_file.path
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        else:
            raise Http404("Fayl topilmadi.")
    except StudentInfo.DoesNotExist:
        raise Http404("Kod noto‘g‘ri.")


def pdf_page(request, code):
    try:
        student_info = StudentInfo.objects.get(file_id=code)
        file_url = student_info.student_file.url
        return render(request, 'pdf_view.html', {'file_url': file_url, 'code': code})
    except StudentInfo.DoesNotExist:
        raise Http404("Kod noto‘g‘ri.")

