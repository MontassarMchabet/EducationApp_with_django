from django.shortcuts import render, redirect, get_object_or_404
from .models import Chapter
from .forms import ChapterForm
from Course.models import Course

def chapter_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    chapters = Chapter.objects.filter(course=course).order_by('order')
    return render(request, 'chapter/chapter_list.html', {'chapters': chapters, 'course': course})

def create_chapter(request):
    if request.method == "POST":
        form = ChapterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chapter_list')
    else:
        form = ChapterForm()
    return render(request, 'chapter/chapter_form.html', {'form': form})

def update_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    if request.method == "POST":
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            return redirect('chapter_list')
    else:
        form = ChapterForm(instance=chapter)
    return render(request, 'chapter/chapter_form.html', {'form': form})

def delete_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    if request.method == "POST":
        chapter.delete()
        return redirect('chapter_list')
    return render(request, 'chapter/chapter_confirm_delete.html', {'chapter': chapter})
