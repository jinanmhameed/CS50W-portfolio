from django.shortcuts import render
from . import util
import markdown2
from django.shortcuts import redirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page does not exist."
        })
    
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get("q", "").strip().lower()
    entries = util.list_entries()
    
    # בדיקה אם יש התאמה מדויקת
    for entry in entries:
        if entry.lower() == query:
            return redirect("entry", title=entry)

    # התאמות חלקיות
    matches = [entry for entry in entries if query in entry.lower()]
    
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "matches": matches
    })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })
        
        util.save_entry(title, content)
        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("entry", title=title)

    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

import random

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect("entry", title=title)
