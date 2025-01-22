# Goodreads Book Data Automation

#### Video Demo:  <https://youtu.be/Csjh-zPIDEA>

## Description

This program is my final project for **HarvardX CS50P: Introduction to Programming with Python**.

I created a tool that automates the extraction of genre, format, and audience classification data from Goodreads books using their book IDs, offering helpful qualitative insights for large datasets. This tool was designed to address the limitations of Goodreads' data export, which doesn’t include all qualitative data available on the platform.

The need for this tool originated from my personal experience creating a "Reading Wrapped" data summary for the books I read in a year. Goodreads’ data exports lack some qualitative information, which I had to manually add last year, such as author gender, main character diversity, book genre, book format, and book audience. Some of this information is available on individual Goodreads book pages (i.e., the latter three data points), so this tool aims to streamline the process of getting that information, especially for users analyzing large datasets from Goodreads.

## Features

- Extracts top 3 genres for each book.
- Uses genre data to identify **book format** and **audience information** and separates them into their own columns, improving data accuracy.
- Accepts **book IDs** as input, making it convenient for users analyzing their Goodreads data.
- Filters out **duplicate book IDs**.
- Identifies **invalid book IDs** and allows users to correct them to ensure data integrity.
- Excludes the term **“Audiobooks”** from the genre and format lists. This ensures more accurate data as "audiobooks" is neither a genre nor a standard book format.
- Saves organized book data in a structured **CSV file** for easy export and analysis.

## Practical Application

For users looking to analyze their Goodreads data and want to save time on manual data entry, this program:

1. Supports book ID input, which is quicker and more practical than URLs for batch processing because Goodreads gives you book IDs (with other information) when you export your reading data from their platform.
2. Offers detailed breakdowns of formats (e.g., Novella, Graphic Novel) and audience types (e.g., Young Adult, Children's).
3. Shows you the top 3 genres per book, so you can choose which genre labels you prefer for your analysis.
4. Gives you a CSV with all the extracted data per book that you can easily combine with the rest of your Goodreads data export.

## Installation

1. Clone the project files.
2. Install the required dependencies (requests and beautifulsoup4) using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run `python project.py`

2. Enter a list of Goodreads Book IDs as a comma-separated list. Example input: `63024319, 207004036, 63028652`.

3. The output will be a table and a CSV file called `book_data.csv` with the following details for each book:
  - Book ID
  - Title
  - Format
  - Audience
  - Top 3 Genres

Example table:

![image](https://github.com/user-attachments/assets/aa0073b6-4ce7-4a94-8e0d-74899e9d1eca)


## Testing

The project includes extensive unit tests using pytest to ensure data reliability. These tests check:

- Book genre extraction with `get_genres`.
- Book title retrieval with `get_book_title`.
- Duplicate book ID removal and handling invalid IDs.
- The CSV file is saved correctly.

To run the tests, use:
```bash
pytest test_project.py
```

### Tests Included:
- **Test for determine_format:**
Ensures the function correctly identifies book formats from genre lists.

- **Test for determine_audience:**
Ensures the function classifies book audiences correctly from genre lists.

- **Test for handling duplicates:**
Ensures that duplicate book IDs are removed from the list correctly.

- **Test for handling invalid book IDs:**
Ensures that invalid or nonexistent book IDs are filtered out.

- **Test for get_book_title:**
Ensures valid book titles are returned when using a real network request.

- **Test for get_genres:**
Ensures that genre data is correctly fetched using real network requests.

- **Test for save_to_csv:**
Ensures that the CSV file is generated properly with the correct data. Temporary files are used to validate if the file is saved and the content matches the expected format.


## Notes on Design Choices

The program initially prompted users for one Goodreads URL at a time and outputted the URL with the book’s top 3 genres. After thinking more about how the tool should work practically, I made three decisions:

1. **Prompt users for a list of comma-separated book IDs** instead of individual URLs. For the target audience (i.e., users who have exported their Goodreads data and want the qualitative data my tool can pull), that’s easier than entering individual URLs because the IDs are included in Goodreads data exports. Then, the CSV output can be imported into spreadsheet programs for further analysis, making it more user-friendly.

2. **Separate book format and audience from genres.** While testing the initial program, I noticed sometimes book format (such as a book being a “graphic novel” or a “picture book”) and book audience (such as a book having a “middle-grade” audience or a “young adult” audience) were among the top genres despite these not being real genres. I thought it would be more helpful for me and other users if these data points were removed from the top genres list and separated into their own columns. This made the final genre list more accurate and reliable while giving users additional relevant qualitative data points about the books they read.

3. **Exclude “Audiobooks” from the genre list.** Because a book’s genre list is the basis for the rest of the qualitative data in the output, and “Audiobooks” is neither a genre nor the original format books are usually published in, the data is more reliable when “Audiobooks” is excluded from the final lists.
