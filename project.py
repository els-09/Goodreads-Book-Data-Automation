import requests
from bs4 import BeautifulSoup
import csv

class BookNotFoundError(Exception):
    """Custom exception raised when a book ID doesn't exist."""
    pass

def get_genres(url):
    """Scrape top 6 genres from a Goodreads book page."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return []  # Return empty list if there's any error (including 404)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find genres from the page
    genres = []
    genre_tags = soup.find_all('a', class_='Button Button--tag Button--medium')

    for tag in genre_tags[:6]:  # Get top 6 genres
        genre = tag.find('span', class_='Button__labelItem').text.strip()

        # Exclude genres with dashes (indicating a bookshelf tag)
        if '-' in genre:
            continue

        genres.append(genre)

    # Exclude "Audiobook"
    genres = [genre for genre in genres if genre.lower() != 'audiobook']

    return genres

def get_book_title(url):
    """Scrape the title of the book from the Goodreads page."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None  # Return None if there's any error (including 404)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the book title using the provided class
    title_tag = soup.find('h1', class_='Text Text__title1')

    if title_tag:
        return title_tag.text.strip()  # Return the title in title case
    else:
        return None  # Return None if title is not found

def print_table(data):
    """Prints the data in a nice ASCII table format."""
    print(f"{'Book ID':<10} {'Title':<50} {'Format':<15} {'Audience':<15} {'Genre 1':<20} {'Genre 2':<20} {'Genre 3':<20}")
    print("-" * 135)

    for row in data:
        print(f"{row['Book ID']:<10} {row['Title']:<50} {row['Format']:<15} {row['Audience']:<15} {row['Genre 1']:<20} {row['Genre 2']:<20} {row['Genre 3']:<20}")
    print("\n")

def save_to_csv(data, file_path='book_data.csv'):
    """Save the collected data to a CSV file."""
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Book ID', 'Title', 'Format', 'Audience', 'Genre 1', 'Genre 2', 'Genre 3'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    # Specify the file path where the CSV will be saved
    print(f"Data has been saved to '{file_path}'.")

def determine_format(genres):
    """Determine the 'Format' value based on the genres."""
    format_keywords = ['Graphic Novels', 'Picture Books', 'Novella', 'Novel', 'Short Stories']
    for genre in genres:
        if genre in format_keywords:
            return genre
    return "Novel"  # Default to "Novel" if none of the format-specific genres are found

def determine_audience(genres):
    """Determine the 'Audience' value based on the genres."""
    audience_keywords = ['Childrens', 'Middle Grade', 'Young Adult']
    for genre in genres:
        if genre in audience_keywords:
            return genre
    return "Adult"  # Default to "Adult" if none of the audience-specific genres are found

def process_book(book_id):
    """Process a single book ID and return the data row if valid, or None if invalid."""
    url = f'https://www.goodreads.com/book/show/{book_id}'

    # Get book title
    book_title = get_book_title(url)
    if not book_title:
        return None

    # Get genres
    genres = get_genres(url)
    if not genres:
        return None

    # Determine format and audience
    format_value = determine_format(genres)
    audience_value = determine_audience(genres)

    # Adjust genres based on format or audience
    if format_value in genres:
        genres.remove(format_value)
    if audience_value in genres:
        genres.remove(audience_value)

    while len(genres) < 3:
        genres.append('N/A')

    return {
        'Book ID': book_id,
        'Title': book_title,
        'Format': format_value,
        'Audience': audience_value,
        'Genre 1': genres[0],
        'Genre 2': genres[1],
        'Genre 3': genres[2]
    }

def main():
    # Enter list of book IDs
    book_ids = input("Enter a list of Goodreads book IDs (comma-separated): ").strip().split(',')

    # Remove extra spaces from IDs and de-duplicate initially
    book_ids = list(set(book_id.strip() for book_id in book_ids))

    data = []
    processed_ids = set()

    while True:
        # Track invalid IDs in this iteration
        current_invalid_ids = []

        # Process each book ID
        for book_id in book_ids:
            if book_id in processed_ids:
                continue  # Skip already processed IDs
            result = process_book(book_id)
            if result:
                data.append(result)
                processed_ids.add(book_id)  # Add only valid IDs to processed set
            else:
                current_invalid_ids.append(book_id)

        if current_invalid_ids:
            print(f"\nThe following book IDs were invalid: {', '.join(current_invalid_ids)}")
            new_ids = input("Re-enter corrected book IDs (or type 'done' to exit): ").strip()

            if new_ids.lower() == 'done':
                # Exit if no valid data exists or the user opts out
                if not data:
                    print("Exiting: No valid book data provided.")
                break

            # Update book_ids with re-entered IDs, excluding already processed ones
            book_ids = list(set(new_ids.split(',')))
            book_ids = [book_id.strip() for book_id in book_ids if book_id.strip()]
        else:
            # Exit the loop when there are no invalid IDs
            break

    # Output results and save to CSV
    if data:
        print_table(data)
        save_to_csv(data)
    else:
        print("Exiting: No valid book data to process.")

if __name__ == "__main__":
    main()
