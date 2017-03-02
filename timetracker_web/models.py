"""Models for time tracker web app."""

from timetracker.models import Category, Task


def appmaker(zodb_root):
    """Find root of application, creating if not present."""

    root_key = 'vi'

    if root_key not in zodb_root:
        app_root = Category(root_key, "Tasks")
        zodb_root[root_key] = app_root
        import transaction
        transaction.commit()
    zodb_root[root_key].id = ""
    return zodb_root[root_key]
