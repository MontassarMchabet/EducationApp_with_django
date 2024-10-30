from django.shortcuts import render, redirect, get_object_or_404
from .models import Page
from .forms import PageForm
from .models import Chapter

def page_list(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    pages = Page.objects.filter(chapter=chapter).order_by('order')
    return render(request, 'page/page_list.html', {'pages': pages, 'chapter': chapter})

def page_detail(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    context = {
        'page': page,
    }
    return render(request, 'page/page_detail.html', context)

def create_page(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page = form.save(commit=False)
            page.chapter = chapter
            page.save()
            return redirect('page_list', chapter_id=chapter.id)
    else:
        form = PageForm()

    pages = Page.objects.filter(chapter=chapter).order_by('order')
    return render(request, 'page/page_list.html', {'form': form, 'chapter': chapter, 'pages': pages})

def update_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('page_list', chapter_id=page.chapter.id)
    else:
        form = PageForm(instance=page)

    return render(request, 'page/page_list.html', {'form': form, 'page': page})

def delete_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == "POST":
        page.delete()
        return redirect('course_list')
    return render(request, 'page/page_confirm_delete.html', {'page': page})
