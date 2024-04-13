"""Functionality for Part import template.

Primarily Part import tools.
"""

from InvenTree.helpers import DownloadFile, GetExportFormats

from .models import Part


def IsValidPartFormat(fmt):
    """Test if a file format specifier is in the valid list of part import template file formats."""
    return fmt.strip().lower() in GetExportFormats()


def MakePartTemplate(fmt):
    """Generate a part import template file (for user download)."""
    fmt = fmt.strip().lower()

    if not IsValidPartFormat(fmt):
        fmt = 'csv'

    # TODO implement exporter
    data = ''.encode()
    filename = 'InvenTree_Part_Template.' + fmt
    return DownloadFile(data, filename)
