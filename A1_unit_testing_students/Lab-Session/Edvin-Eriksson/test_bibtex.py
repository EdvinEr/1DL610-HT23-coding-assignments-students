import bibtex
import pytest

@pytest.fixture
def setup_data():
    return {
        'simple_author_1': "Smith",
        'simple_author_2': "Jones",
        'author_1': "John Smith",
        'author_2': "Bob Jones",
        'author_3': "Justin Kenneth Pearson",
        'surname_first_1': "Pearson, Justin Kenneth",
        'surname_first_2': "Van Hentenryck, Pascal",
        'multiple_authors_1': "Pearson, Justin and Jones, Bob"
    }

def test_author_1(setup_data):
    # Test only surnames
    surname, first_names = bibtex.extract_author(setup_data['simple_author_1'])
    assert (surname, first_names) == ('Smith', '')

    surname, first_names = bibtex.extract_author(setup_data['simple_author_2'])
    assert (surname, first_names) == ('Jones', '')

def test_author_2(setup_data):
    # Test simple first name author
    surname, first = bibtex.extract_author(setup_data['author_1'])
    assert (surname, first) == ("Smith", "John")

    surname, first = bibtex.extract_author(setup_data['author_2'])
    assert (surname, first) == ("Jones", "Bob")

def test_author_3(setup_data):
    surname, first = bibtex.extract_author(setup_data['author_3'])
    assert (surname, first) == ("Pearson", "Justin Kenneth")

def test_surname_first(setup_data):
    surname, first = bibtex.extract_author(setup_data['surname_first_1'])
    assert (surname, first) == ("Pearson", "Justin Kenneth")

    surname, first = bibtex.extract_author(setup_data['surname_first_2'])
    assert (surname, first) == ("Van Hentenryck", "Pascal")

def test_multiple_authors(setup_data):
    authors = bibtex.extract_authors(setup_data['multiple_authors_1'])
    assert authors[0] == ('Pearson', 'Justin')
    assert authors[1] == ('Jones', 'Bob')