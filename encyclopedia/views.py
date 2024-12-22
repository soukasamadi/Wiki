from django.shortcuts import render, redirect

from . import util
import markdown2, re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content:
        content_html = markdown2.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "content" : content_html
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "message" : f"The entry '{title}' was not found."
        })
        
def  search(request):
    query = request.GET.get("q", "").strip() #Get the query entered by the user

    if not query:
        return render(request, "encyclopedia/search.html", {
            "entries": [],
            "query": query 
        })

    entries = util.list_entries() #Get all entries

    #Check for an exact match
    if query.lower() in (entry.lower() for entry in entries):
        return redirect("entry", title=query)
    #search for entries containing the query as a substring
    else:
        substring_entries = [entry for entry in entries if re.search(query, entry, re.IGNORECASE)]
        return render(request, "encyclopedia/search.html", {
            "entries": substring_entries,
            "query": query
        })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        #Check if the page already exists
        if util.get_entry(title):
            return render(request, "encyclopedia/new_page.html", {
                "error": "an encyclopedia entry already exists with the provided title.",
                "title": title,
                "content": content
            })

        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            util.save_entry(title, content)
            return redirect("entry", title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            return render (request, "encyclopedia/error.html", {
                "message": "The requested page does not exist. "
            })

        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content,
        })                     

