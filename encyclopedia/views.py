from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from . import util

class NewEntryForm(forms.Form):
    entryName = forms.CharField(label="Title")
    entryContent = forms.CharField(widget=forms.Textarea(attrs={'size': '20'}), label="Content")

class EditForm(forms.Form):
    entryName = forms.CharField(label="Edit Title")
    entryContent = forms.CharField(widget=forms.Textarea(attrs={'size': '20'}), label="Edit Content")

def index(request):
    # If Search
    if request.method == "POST":
        searchterm = request.POST['q']
        entries = util.list_entries()
        # list = all matches
        list = util.search_entries(searchterm, entries)
        # If there is an exact match, redirect
        for item in list:
            if item.lower() == searchterm.lower():
                return HttpResponseRedirect(f"wiki/{item}")
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": list,
                "search": True
            })

    # If not Search
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if request.method == "POST":
        entry = request.POST['q']
        return HttpResponseRedirect(f"{entry}")
    return render(request, "encyclopedia/entry.html", {
        "entryName": entry,
        "entryContent": util.get_entry(entry)
    })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entryName"]
            content = form.cleaned_data["entryContent"]
            if not util.entry_exists(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(f"wiki/{title}")
            else:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": 1
                })
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })

def edit(request, entry):
    if request.method == "POST":
        entry = request.POST['entry']
        content = request.POST['content']
        util.save_entry(entry, content)
        return HttpResponseRedirect(f"/wiki/{entry}")
    content = util.get_entry(entry, True)
    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "content": content
    })

def random(request):
    # If Search
    if request.method == "POST":
        entry = request.POST['q']
        return HttpResponseRedirect(f"wiki/{entry}")
    # Else Random
    e = util.random_entry()
    return render(request, "encyclopedia/random.html", {
        "randomEntry": e,
        "entryContent": util.get_entry(e)
    })
