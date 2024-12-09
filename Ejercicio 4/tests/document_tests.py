import pytest
from models.document import TextDocument

def test_text_document_initialization():
    doc = TextDocument("This is a test document.")
    assert doc.getId() == 1
    assert doc.get_content() == "This is a test document."
    assert str(doc) == "Documento 1: This is a test document...."

def test_text_document_increase_id():
    doc1 = TextDocument("First document.")
    doc2 = TextDocument("Second document.")
    assert doc1.getId() == 2
    assert doc2.getId() == 3

def test_text_document_str():
    doc = TextDocument("Another test document with more than thirty characters.")
    assert str(doc) == "Documento 4: Another test document with mo..."

def test_text_document_get_content():
    content = "Sample content for testing."
    doc = TextDocument(content)
    assert doc.get_content() == content

def test_text_document_get_id():
    doc = TextDocument("Testing ID retrieval.")
    assert doc.getId() == 5