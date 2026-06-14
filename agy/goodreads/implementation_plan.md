# Automatically Fetch and Sync Goodreads Books

This plan details the implementation of an automated script and GitHub Actions workflow to fetch all books you read from your public Goodreads profile, categorize them into the site's existing book categories, add a professional first-person comment highlighting your proactivity in learning, and automatically download the book covers.

## User Review Required

> [!NOTE]
> - **Initial Populate**: The script will include pre-written, high-quality comments and categories for your existing 40 read books on Goodreads so you don't need a Gemini API key to bootstrap.
> - **Future Automation**: To dynamically categorize and write comments for *new* books you read in the future, you will need to add a `GEMINI_API_KEY` secret in your GitHub repository settings. If no API key is provided, the script will fall back to a default category and generic comment structure so it never fails.
> - **GitHub Action Permissions**: The GitHub Actions workflow will require `contents: write` permission to commit and push the new markdown files and cover images to the repository automatically.

## Proposed Changes

### [Goodreads Book Sync Script]

#### [NEW] [fetch_goodreads_books.py](file:///Users/gabripo/github/portfolio/scripts/fetch_goodreads_books.py)
A Python script utilizing Python's standard library (`urllib`, `xml.etree.ElementTree`) to:
1. Fetch your public Goodreads RSS feed (`https://www.goodreads.com/review/list_rss/135131678`).
2. Parse the items and filter for books that are read (excluding `to-read` and `currently-reading`).
3. Match against a pre-crafted mapping for your existing 40 books.
4. For new/future books, call the Gemini API if `GEMINI_API_KEY` is present, or fallback gracefully.
5. Create a Hugo-compatible Markdown file under `content/book/{slug}.md`.
6. Run `go run scripts/fetch_book_covers.go` at the end to download any missing covers.

### [GitHub Actions Workflow]

#### [NEW] [sync-goodreads.yml](file:///Users/gabripo/github/portfolio/.github/workflows/sync-goodreads.yml)
A scheduled GitHub Actions workflow (running weekly or manually triggered) that:
1. Checks out the repository (with submodules).
2. Sets up Python and Go.
3. Installs dependencies (if any, though standard library Python requires none).
4. Runs the book sync script.
5. Commits and pushes any new book markdown files and cover images back to the `main` branch.

## Verification Plan

### Automated Tests
- We will run the Python script locally to populate the `content/book` directory.
- We will verify that `go run scripts/fetch_book_covers.go` successfully downloads covers.
- We will run `hugo` to confirm the site builds successfully with the newly added books.
- We will verify the links and categories on the generated books list page.
