import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown


def list_entries(query=None):
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    if not query:
        query = "."
    return list(sorted(re.sub(r"\.md$", "", filename)
                       for filename in filenames
                       if filename.endswith(".md")
                       and query in filename.lower()))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_html_entry(title):
    markdown = get_entry(title)
    html = markdown_to_html(markdown)
    return html


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def markdown_to_html(markdown):
    converter = Markdown()
    return converter.convert(text=markdown)
