#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from scripts.id_card_utils import initialize_id_printer

def main():
    initialize_id_printer() # note: this will run twice, since the auto-reloader runs as a separate process

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtv_site.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
