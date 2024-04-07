from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util
from random import choice


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title", max_length=30)
    content = forms.CharField(label="", widget=forms.Textarea)


def index(request):
    query = request.GET.get('q')
    if query:
        if util.get_entry(query):
            return HttpResponseRedirect(reverse("entry", args=(query,)))
        else:
            return render(request, "encyclopedia/search.html", {
                "entries": util.list_entries(query)
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": util.get_html_entry(title)
        })
    else:
        return render(request, "encyclopedia/notFound.html", {
            "title": title,
            "content": "<p>Requested entry not found</p>"
        })


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if not util.get_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", args=(title,)))
        return render(request, "encyclopedia/new.html", {
            "form": form,
            "message": "Such entry already exists."
        })

    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })


def edit(request, title):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": title,
            "message": "Invalid entry."
        })

    initial_data = {'title': title, 'content': util.get_entry(title)}
    form = NewEntryForm(initial=initial_data)
    form.fields["title"].widget.attrs = {"readonly": "True"}

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title,
    })


def random(request):
    entries = util.list_entries()
    selected_entry = choice(entries)
    return HttpResponseRedirect(reverse("entry", args=(selected_entry,)))
