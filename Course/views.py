from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from .forms import CourseForm
from django.contrib import messages



def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', {'courses': courses})

def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'course/course_list.html', {'form': form})


def update_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect('course_list')  # Redirect to the course list view
    else:
        form = CourseForm(instance=course)
    return render(request, 'course/course_list.html', {'form': form, 'course': course})

def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect('course_list')  # Redirect to the course list view
    return redirect('course_list')
