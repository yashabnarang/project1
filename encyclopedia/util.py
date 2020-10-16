import re
import random
import markdown2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def search_entries(searchterm, entries):
    list = []
    for entry in entries:
        if entry.lower().find(searchterm.lower()) != -1:
            list.append(entry)
    return list


def random_entry():
    """
    Returns 1 random name from encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    l = list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))
    return random.choice(l)


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


def get_entry(title, raw=False):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        if not raw:
            return markdown2.markdown(f.read().decode("utf-8"))
        else:
            return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def entry_exists(title):
    return default_storage.exists(f"entries/{title}.md")
