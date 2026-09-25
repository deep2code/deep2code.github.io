#!python3
# -*- coding:utf8 -*-

book_path = "~/git-code/github/reference/book"
pdf_path = "~/git-code/github/reference/pdf"

# py_pdf_path = "~/git-code/docs-pdf"

import os

# from PyPDF2 import PdfMerger

# merger = PdfMerger()

# for root, dirs, files in os.walk(py_pdf_path):
#     for name in files:
#         if not name.endswith(".pdf"):
#             continue
#         merger.append(os.path.join(root, name))

# merger.write("python-3.10.8.pdf")
# merger.close()

# import sys

# sys.exit(0)


# for root, dirs, files in os.walk(book_path, topdown=False):
#     for name in files:
#         if not name.endswith(".html"):
#             continue
#         print("html:", name, os.path.join(root, name))

#         import os

#         os.system(
#             "wkhtmltopdf {} {}".format(
#                 os.path.join(root, name), os.path.join(pdf_path, name)
#             )
#         )

for root, dirs, files in os.walk(pdf_path, topdown=False):
    for name in files:
        if name.endswith(".html"):
            new_name = name.replace(".html", ".pdf")
            os.rename(os.path.join(root, name), os.path.join(root, new_name))


from PyPDF2 import PdfMerger

merger = PdfMerger()

for root, dirs, files in os.walk(pdf_path, topdown=False):
    for name in files:
        if name.endswith(".pdf"):
            merger.append(os.path.join(root, name))

merger.write("rust.pdf")
merger.close()
