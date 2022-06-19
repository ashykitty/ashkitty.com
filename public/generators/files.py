import os
from app import *

def generate( page, request):
    files = os.listdir("public/files/")

    files = "\n".join([f"<a href=\"/{a}\">{a}</a><br>" for a in files])

    return page.replace( "{FILES}", files)
