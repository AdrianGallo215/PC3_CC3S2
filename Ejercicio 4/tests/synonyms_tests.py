import pytest
from synonyms import getSynonyms

def test_getSynonyms():
    phrase = "feliz"
    synonyms = getSynonyms(phrase)
    assert isinstance(synonyms, list)
    assert "contento" in synonyms or "alegre" in synonyms

def test_getSynonyms_empty():
    phrase = ""
    synonyms = getSynonyms(phrase)
    assert synonyms == []

def test_getSynonyms_nonexistent():
    phrase = "nonexistentword"
    synonyms = getSynonyms(phrase)
    assert synonyms == []

if __name__ == "__main__":
    pytest.main()