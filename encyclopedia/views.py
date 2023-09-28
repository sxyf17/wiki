from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown2
from . import util
import random
from django import forms


class newEntryForm(forms.Form):
    entryForm = forms.CharField(label="New Entry")


def md_to_html(title):
    content = util.get_entry(title)
    
    if content == None:
        return None
    else:
        return markdown2.markdown(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    
    html_entry = md_to_html(title)
    if html_entry == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page Could Not Be Found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_entry
        })
    
def search(request):
    if request.method == "POST":
        query = request.POST['q']
        html_content = md_to_html(query)
        
        entries = util.list_entries()
        results = []
        for entry in entries:
            if query.lower() in entry.lower():
                results.append(entry)
        
        if html_content is not None:
            if query.capitalize() in entries:
                return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": html_content
                })
        
        else:
            if results:
                return render(request, "encyclopedia/search.html", {
                    "results": results
                })
            else:
                return render(request, "encyclopedia/search.html")
            
def randEntry(request):
    entries = util.list_entries()
    all_entries = {}
    
    i = 0
    for entry in entries: #assigns each entry a number
        all_entries[i] = entry
        i+=1
    rand = random.randint(0,i-1) #chooses random number
    newEntry = all_entries.get(rand) #gets entry with that number
    return redirect('entry', title=newEntry)

def newEntry(request):
    if request.method == "GET":    
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry Page Already Exists"
            })
        else:
            util.save_entry(title,content)
            html_content = md_to_html(content)
            return redirect('entry', title=title)
            
def editEntry(request):
    
    if request.method == "POST":
        title = request.POST["title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
        
def saveEntry(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content) 
        html_content = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
        
        
            
        