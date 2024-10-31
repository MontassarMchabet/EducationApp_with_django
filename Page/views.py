from django.shortcuts import render, redirect, get_object_or_404
from .models import Page
from .forms import PageForm
from .models import Chapter
import requests

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

# def create_page(request, chapter_id):
#     chapter = get_object_or_404(Chapter, pk=chapter_id)
#     if request.method == "POST":
#         form = PageForm(request.POST, request.FILES)
#         if form.is_valid():
#             page = form.save(commit=False)
#             page.chapter = chapter
#             page.save()
#             return redirect('page_list', chapter_id=chapter.id)
#     else:
#         form = PageForm()

#     pages = Page.objects.filter(chapter=chapter).order_by('order')
#     return render(request, 'page/page_list.html', {'form': form, 'chapter': chapter, 'pages': pages})

SERVICE_ID = 'sWfUvP6BJxzjfh4'
API_URL = 'https://svc.webspellchecker.net/api'

def create_page(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page = form.save(commit=False)
            page.chapter = chapter
            
            # Check the content using WebSpellChecker API
            content_to_check = form.cleaned_data["content"]
            api_response = check_content_with_webspellchecker(content_to_check)

            print("API Response:", api_response)  # Print the API response for debugging
            
            # Extract corrected content from the API response (if applicable)
            corrected_content = content_to_check  # Default to original content
            
            if api_response and 'result' in api_response:
                # Make sure there's at least one result before accessing
                if api_response['result']:
                    corrections = api_response['result'][0].get('matches', [])
                    
                    # Sort corrections by offset in descending order
                    corrections.sort(key=lambda x: x['offset'], reverse=True)
                    
                    for correction in corrections:
                        start = correction['offset']
                        length = correction['length']
                        
                        # Use a safe approach to get suggestions
                        suggestions = correction.get('suggestions', [])
                        suggestion = suggestions[0] if suggestions else ''  # Take the first suggestion if available
                        
                        print(f"Correction found: {correction}, Suggestion: {suggestion}")  # Debugging output
                        
                        # Apply correction only if suggestion is valid
                        if suggestion:
                            corrected_content = (
                                corrected_content[:start] +
                                suggestion +
                                corrected_content[start + length:]
                            )
                        else:
                            print("No suggestions found for this correction.")
            
            page.content = corrected_content  # Set the corrected content
            page.save()
            return redirect('page_list', chapter_id=chapter.id)
    else:
        form = PageForm()

    pages = Page.objects.filter(chapter=chapter).order_by('order')
    return render(request, 'page/page_list.html', {'form': form, 'chapter': chapter, 'pages': pages})

def check_content_with_webspellchecker(content):
    """
    Check content using WebSpellChecker API.
    """
    payload = {
        'cmd': 'check',
        'text': content,
        'customerid': SERVICE_ID
    }
    
    try:
        response = requests.post(API_URL, data=payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response
    except requests.RequestException as e:
        print(f"Error calling WebSpellChecker API: {e}")
        return None

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
