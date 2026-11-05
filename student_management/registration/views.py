from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student


def student_registration(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
    else:
        form = StudentForm()

    return render(request, 'registration/registration.html', {'form': form})


def registration_success(request):
    return render(request, 'registration/success.html')


def student_list(request):
    students = Student.objects.order_by('last_name', 'first_name')
    return render(request, 'registration/student_list.html', {'students': students})


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'registration/student.detail.html', {'student': student})


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()

    return render(request, 'registration/student_form.html', {
        'form': form,
        'title': 'Add student',
    })


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)

    return render(request, 'registration/student_form.html', {
        'form': form,
        'student': student,
        'title': 'Edit student',
    })


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    return render(request, 'registration/student_confirm_delete.html', {'student': student})