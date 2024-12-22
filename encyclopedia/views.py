from django.shortcuts import render

from . import util
import markdown2


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

