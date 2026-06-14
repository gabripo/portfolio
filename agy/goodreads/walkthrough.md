# Walkthrough: Goodreads Books Integration and Automation

I have built a robust, automated synchronization system that imports books from your public Goodreads profile, categorizes them using your site's existing categories, downloads their covers directly, and commits them to your site.

## Changes Made

### 1. Goodreads Sync Script
- **Added** [fetch_goodreads_books.py](file:///Users/gabripo/github/portfolio/scripts/fetch_goodreads_books.py):
  - Fetches and parses your public Goodreads RSS feed.
  - Automatically filters for books that you have read (skipping `to-read` and `currently-reading`).
  - Contains a pre-crafted database mapping of categories and comments for your existing 40 books to bootstrap your site without requiring API key calls.
  - Downloads cover images directly from Goodreads, avoiding rate limits.
  - Supports automatic, dynamic categorization and comment generation using the Google Gemini API for any *new* books you read in the future, if you provide a `GEMINI_API_KEY` in the environment.

### 2. GitHub Actions Workflow
- **Added** [sync-goodreads.yml](file:///Users/gabripo/github/portfolio/.github/workflows/sync-goodreads.yml):
  - Triggers automatically once a week (Sundays at midnight UTC) and can also be triggered manually.
  - Runs the sync script to pull any new books from your Goodreads profile.
  - Automatically commits and pushes new markdown files and covers back to the `main` branch.

### 3. Cover Image Enhancements
- **Enhanced** [fetch_book_covers.go](file:///Users/gabripo/github/portfolio/scripts/fetch_book_covers.go):
  - Improved the query parsing logic to strip out long subtitles and parentheses before searching the Google Books API. This improves API matching success rates.

## Verification & Testing Results

- **Sync Run Success**: Ran the script locally; it parsed the feed, matched the predefined books, and generated 23 read book files under `content/book/`.
- **Direct Cover Downloads**: Successfully downloaded all 23 high-quality book covers directly from Goodreads and saved them under `static/images/books/`.
- **Site Compilation**: Re-ran the local `hugo` build, which successfully compiled the site with 124 pages (up from 53) without any errors.
