from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from .forms import CourseForm
from django.contrib import messages
from .utils import TextSummarizer
from django.http import JsonResponse

text_summarizer = TextSummarizer()  # Initialize the summarizer



def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', {'courses': courses})

# def create_course(request):
#     if request.method == "POST":
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('course_list')
#     else:
#         form = CourseForm()
#     return render(request, 'course/course_list.html', {'form': form})

def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            # Get the course description from the form
            course_description = form.cleaned_data['description']
            
            # Generate summary if description is provided
            summary_result = text_summarizer.summarize_text(course_description)
            
            if summary_result['error']:
                # Handle error in summarization
                return JsonResponse({
                    'error': f"Failed to generate summary: {summary_result['error']}"
                }, status=500)
            
            # Optionally, you can add the summary to the course model
            form.instance.description_summary = summary_result['summary']
            
            # Save the course
            form.save()
            return redirect('course_list')  # Redirect after saving
    else:
        form = CourseForm()  # If GET request, initialize an empty form

    return render(request, 'course/course_form.html', {'form': form})

def update_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            # Get the updated course description from the form
            course_description = form.cleaned_data['description']
            
            # Generate summary if description is provided
            summary_result = text_summarizer.summarize_text(course_description)
            
            if summary_result['error']:
                # Handle error in summarization
                return JsonResponse({
                    'error': f"Failed to generate summary: {summary_result['error']}"
                }, status=500)
            
            # Optionally, you can add the summary to the course model
            form.instance.description_summary = summary_result['summary']
            
            # Save the course
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect('course_list')  # Redirect to the course list view
    else:
        form = CourseForm(instance=course)

    return render(request, 'course/course_form.html', {'form': form, 'course': course})

def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect('course_list')  # Redirect to the course list view
    return redirect('course_list')
