import pytest
import project

# Test format determination
def test_format():
    assert project.determine_format(['Novella', 'Romance', 'Fantasy']) == 'Novella'
    assert project.determine_format(['Short Stories', 'Science Fiction', 'Adventure']) == 'Short Stories'
    assert project.determine_format(['Graphic Novels', 'Fantasy', 'Adventure']) == 'Graphic Novels'
    assert project.determine_format(['Romance', 'Fantasy', 'Novel']) == 'Novel'  # Default to Novel

# Test audience classification
def test_audience():
    assert project.determine_audience(['Young Adult', 'Fantasy', 'Romance']) == 'Young Adult'
    assert project.determine_audience(['Adult Fiction', 'Fantasy', 'Historical']) == 'Adult'
    assert project.determine_audience(['Childrens', 'Fantasy', 'Adventure']) == 'Childrens'
    assert project.determine_audience(['Science Fiction', 'Adventure', 'Romance']) == 'Adult'  # Default to Adult

# Test if duplicate book IDs are removed
def test_handle_duplicates():
    book_ids = ["63024319", "65213699", "63028652", "63024319"]
    unique_ids = list(set(book_ids))
    assert len(unique_ids) == 3
    assert "63024319" in unique_ids
    assert "65213699" in unique_ids
    assert "63028652" in unique_ids

# Test handling of invalid book IDs
def test_handle_invalid_ids():
    book_ids = ["63024319", "00000000"]
    valid_book_ids = [book_id for book_id in book_ids if project.get_book_title(f'https://www.goodreads.com/book/show/{book_id}') is not None]
    assert "00000000" not in valid_book_ids
    assert "63024319" in valid_book_ids

# Test get_book_title with real network request
def test_get_book_title():
    title = project.get_book_title("https://www.goodreads.com/book/show/123456")
    assert title is not None  # Assuming the book exists on Goodreads and can be fetched

# Test get_genres with real network request
def test_get_genres():
    genres = project.get_genres("https://www.goodreads.com/book/show/123456")
    assert len(genres) > 0  # Assuming the book has some genres listed

# Test save_to_csv
def test_save_to_csv(tmp_path):
    # Prepare mock data to be saved
    data = [
        {"Book ID": "63024319", "Title": "Mock Book Title", "Format": "Novel", "Audience": "Young Adult",
         "Genre 1": "Fantasy", "Genre 2": "Adventure", "Genre 3": "Romance"},
        {"Book ID": "65213699", "Title": "Another Mock Book", "Format": "Novel", "Audience": "Young Adult",
         "Genre 1": "Fantasy", "Genre 2": "Adventure", "Genre 3": "Romance"}
    ]

    # Using the tmp_path provided by pytest for temporary files
    file_path = tmp_path / "books_data.csv"

    # Call the function with both the data and the file_path
    project.save_to_csv(data, str(file_path))

    # Validate if the file was created and the content is correct
    with open(file_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 3  # We expect 3 lines: 1 header + 2 rows
        assert "63024319" in lines[1]  # Check that the first book ID is in the second line
