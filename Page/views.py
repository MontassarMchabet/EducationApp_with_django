from django.shortcuts import render, redirect, get_object_or_404
from .models import Page
from .forms import PageForm

def page_list(request):
    pages = Page.objects.all()
    return render(request, 'page/page_list.html', {'pages': pages})

def page_detail(request, chapter_id, page_id):
    page = get_object_or_404(Page, id=page_id)

    # Retrieve previous and next pages
    previous_page = Page.objects.filter(id__lt=page_id, chapter_id=chapter_id).order_by('-id').first()
    next_page = Page.objects.filter(id__gt=page_id, chapter_id=chapter_id).order_by('id').first()

    context = {
        'page': page,
        'previous_page': previous_page,
        'next_page': next_page,
        'chapter_id': chapter_id,  # Pass chapter_id to the template for URL construction
    }
    return render(request, 'page/page_detail.html', context)

def create_page(request):
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES)  # Use request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('page_list')
    else:
        form = PageForm()
    return render(request, 'page/page_form.html', {'form': form})

def update_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES, instance=page)  # Use request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('page_list')
    else:
        form = PageForm(instance=page)
    return render(request, 'page/page_form.html', {'form': form})

def delete_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == "POST":
        page.delete()
        return redirect('page_list')
    return render(request, 'page/page_confirm_delete.html', {'page': page})
