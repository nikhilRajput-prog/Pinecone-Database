import fitz


def load_pdf(pdf_path):
    """
    Extract text from every page of the PDF.

    Returns:
        list of dictionaries containing page number and text.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        if text.strip():

            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()

    return pages