#!/usr/bin/env python3
import os
import re
import urllib.request
import urllib.parse
import csv
import html
import json
import sys

# Config
# Goodreads removed its RSS feeds, so the books come from the library export:
# Goodreads > My Books > Tools: Import and export > Export Library, saved here.
GOODREADS_EXPORT_CSV = "data/goodreads_library_export.csv"
CONTENT_DIR = "content/book"
STATIC_IMG_DIR = "static/images/books"
ALLOWED_CATEGORIES = [
    "Engineering Management",
    "Organization design",
    "Software engineering and development",
    "Technical interview preparation",
    "Product, strategy and business",
    "Leadership",
    "Workplace and culture",
    "Biographies/company stories",
    "Psychology (cognitive, evolutionary, phylosophy...)",
    "Society, world and future",
    "Sport & performance",
    "My reading list"
]

# Pre-crafted database of existing books to avoid needing API key for the first run
PREDEFINED_BOOKS = {
    "how we decide": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "A look at how emotion and reason work together when we decide. It made me more aware of when to trust my gut and when to slow down and check the facts, in negotiations and in engineering trade-offs alike."
    },
    "a whole new mind": {
        "category": "Product, strategy and business",
        "comment": "This book shifted my focus towards holistic, creative thinking. As an engineer, combining structured logical analysis with right-brain empathy and storytelling has significantly enhanced how I collaborate and communicate complex technical sales ideas."
    },
    "to sell is human": {
        "category": "Product, strategy and business",
        "comment": "An eye-opening read that convinced me that 'selling' is a fundamental skill we all practice daily. It has directly refined my technical sales strategies, focusing on attunement, buoyancy, and clarity to align team and customer interests."
    },
    "getting to yes": {
        "category": "Leadership",
        "comment": "A classic guide that completely changed how I approach negotiations and discussions. By focusing on interests rather than positions, I've been able to foster more collaborative, win-win relationships both in my engineering projects and personal life."
    },
    "a book of five rings": {
        "category": "Leadership",
        "comment": "Musashi's timeless principles of discipline, focus, and adaptability offer incredible insights into strategic thinking. Applying these concepts helps me stay calm and structured under pressure, optimizing execution in demanding software and sales environments."
    },
    "the power of regret": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "Pink's exploration of regret helped me view past setbacks as essential lessons for the future. Embracing regret as a constructive tool has made me more proactive in my personal development and decision-making processes."
    },
    "thank you for arguing": {
        "category": "Workplace and culture",
        "comment": "An entertaining yet highly practical masterclass on rhetoric and persuasion. It has helped me improve my presentation skills and navigate corporate debates constructively, ensuring that customer requirements are accurately championed."
    },
    "creativity inc": {
        "category": "Leadership",
        "comment": "A profound look into building and nurturing a creative, risk-tolerant organization. It taught me that keeping feedback loops honest and constructive is key to resolving technical roadblocks and empowering development teams."
    },
    "ikigai": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "These philosophies taught me the value of balance, purpose, and mindfulness. Applying them to my daily routine has significantly boosted my resilience and helped me maintain a healthy work-life balance."
    },
    "the art of war": {
        "category": "Product, strategy and business",
        "comment": "A fundamental text on strategy and conflict resolution. In a business context, it serves as a powerful reminder of the importance of preparation, understanding the competitive landscape, and choosing the right battles to achieve long-term success."
    },
    "gratitude": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "A moving reflection on life, appreciation, and aging. Reading Sacks' thoughts has helped me cultivate a daily practice of gratitude, reminding me to appreciate the learning journey and focus on what truly matters in life."
    },
    "the great gatsby": {
        "category": "My reading list",
        "comment": "A beautifully written critique of ambition, wealth, and the American dream. Engaging with classic fiction like this broadens my cultural perspective and serves as a creative escape that keeps my mind agile and imaginative."
    },
    "mans search for meaning": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "Frankl's profound insights on finding meaning through adversity are deeply inspiring. This book has taught me that we always control our attitude, a mindset that has bolstered my resilience both in personal life and complex engineering roles."
    },
    "norwegian wood": {
        "category": "My reading list",
        "comment": "Murakami's nostalgic and atmospheric storytelling offers a unique look at loss, youth, and relationships. Reading fiction helps me decompress, fostering emotional intelligence and empathy which are vital in customer-facing roles."
    },
    "the magic mountain": {
        "category": "My reading list",
        "comment": "A masterpiece of literature exploring time, sickness, and intellectual ideas. It challenges me to engage with complex narrative structures and deep philosophical questions, which exercises my critical thinking and patience."
    },
    "the intelligent investor": {
        "category": "Product, strategy and business",
        "comment": "The absolute Bible of value investing. It has taught me the importance of analytical discipline, risk management, and long-term thinking—principles that are as vital for commercial engineering decisions as they are for personal finance."
    },
    "12 rules for life": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "A structured approach to taking personal responsibility and establishing order in life. It has reinforced my commitment to structured habits, clear communication, and setting incremental, proactive goals for self-improvement."
    },
    "meditations": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "The ultimate journal on Stoic philosophy. It serves as my guide for maintaining mental clarity, emotional control, and personal integrity under pressure, helping me lead teams and manage customer relations effectively."
    },
    "influence": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "A critical study on the triggers of influence. Understanding these psychological principles has helped me design more convincing sales pitches and communicate value proposals more clearly to customers and stakeholders."
    },
    "the four agreements": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "A simple yet powerful framework for personal conduct. Principles like being impeccable with your word and not taking things personally have improved my communication style and reduced friction in professional team settings."
    },
    "thinking fast and slow": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "A seminal work on cognitive biases and decision-making. As an engineer, understanding System 1 and System 2 thinking has made me more aware of unconscious shortcuts, refining my analytical problem-solving and validation processes."
    },
    "the 80 20 principle": {
        "category": "Product, strategy and business",
        "comment": "This book revolutionized my time management by helping me focus on the few tasks that yield the most impact. Applying Pareto's law has streamlined my daily engineering workflow, optimizing productivity and focus."
    },
    "astrophysics for people in a hurry": {
        "category": "My reading list",
        "comment": "A brief, fascinating summary of our cosmos. Reading about the universe keeps me curious about science and technology, reminding me of the importance of continuous learning and looking at problems from a wider perspective."
    },
    "start with why": {
        "category": "Leadership",
        "comment": "Sinek's concept of the Golden Circle has shaped how I communicate value. Whether pitching a technical solution or aligning a team, starting with the core purpose ('Why') ensures stronger engagement and trust."
    },
    "what we owe the future": {
        "category": "Society, world and future",
        "comment": "An inspiring look at longtermism and how our present choices affect future generations. It motivates me to build high-quality, sustainable solutions and contribute positively to engineering practices that last."
    },
    "sapiens": {
        "category": "Society, world and future",
        "comment": "An engaging overview of human history and the myths that unite us. It has broadened my understanding of human networks, cooperation, and belief systems, which are key to understanding organizational behavior."
    },
    "stop overthinking": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "A highly practical book offering techniques to manage stress and stay focused. Learning to quiet my mind has directly boosted my focus during intense engineering sprints and complex commercial negotiations."
    },
    "eat that frog": {
        "category": "Workplace and culture",
        "comment": "Tracy's focus on prioritizing the most challenging task first has dramatically improved my productivity. Tackling the 'frog' first thing in the morning ensures consistent progress on key engineering objectives."
    },
    "the 7 habits of highly effective people": {
        "category": "Leadership",
        "comment": "A foundational text for personal and professional effectiveness. Habits like being proactive and seeking first to understand before being understood have shaped my leadership style and team collaboration mindset."
    },
    "the quick easy way to effective speaking": {
        "category": "Leadership",
        "comment": "Carnegie's practical tips on public speaking have helped me overcome stage fright and present ideas with impact. It has been invaluable for technical sales pitches, where clear communication is vital to project success."
    },
    "endless referrals": {
        "category": "Product, strategy and business",
        "comment": "An excellent guide to relationship-based selling. It has refined my approach to technical sales, showing me how to build genuine trust and add value to my professional network rather than just pitching products."
    },
    "the awful german language": {
        "category": "My reading list",
        "comment": "Twain's humorous take on the complexities of learning German is both entertaining and reassuring. As someone working in Switzerland and speaking German, it reminds me to embrace the challenges of language learning with a smile."
    },
    "the art of learning": {
        "category": "Sport & performance",
        "comment": "Waitzkin's insights on mastering skills through micro-steps and self-awareness are incredibly powerful. Applying his methodology helps me learn new programming frameworks and sales techniques systematically and efficiently."
    },
    "atomic habits": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "This book taught me how tiny, 1% improvements compound over time. Designing systems to support positive habits has optimized my daily routine, ensuring continuous learning and high personal productivity."
    },
    "rich dad poor dad": {
        "category": "Product, strategy and business",
        "comment": "An eye-opening introduction to financial literacy and asset building. It has influenced my personal finance strategies and given me a business-owner mindset that helps me understand customers' financial incentives."
    },
    "think and grow rich": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "A classic guide to mindset and persistence. It has taught me the value of a definite major purpose and keeping a positive, persistent attitude, motivating me to pursue challenging goals in both life and career."
    },
    "the subtle art of not giving a fck": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "Manson's realistic look at personal values helped me focus my energy on what truly matters. It has taught me to accept constructive feedback and focus on key priorities rather than trivial distractions."
    },
    "how to stop worrying and start living": {
        "category": "Psychology (cognitive, evolutionary, phylosophy...)",
        "comment": "A timeless collection of practical tips for managing stress and anxiety. Applying Carnegie's principles helps me maintain focus and make rational, calm decisions under tight project deadlines."
    },
    "drive": {
        "category": "Workplace and culture",
        "comment": "Pink's focus on autonomy, mastery, and purpose completely aligned with my view on work. Recognizing these intrinsic drivers has helped me keep myself motivated and better support the autonomy of my teams."
    },
    "how to win friends influence people": {
        "category": "Leadership",
        "comment": "The gold standard for interpersonal relations. Its principles, such as showing genuine interest in others and avoiding criticism, are fundamental to my day-to-day interactions in technical sales and team collaboration."
    },
    "never split the difference": {
        "category": "Product, strategy and business",
        "comment": "An outstanding negotiation manual based on real-world FBI hostage tactics. Voss's techniques, like tactical empathy and calibrated questions, have been game-changing for commercial negotiations and technical sales."
    }
}

def normalize_title(title):
    main_title = re.split(r'[:\(]', title)[0]
    normalized = main_title.lower()
    normalized = re.sub(r'[^a-z0-9\s]+', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized.strip()

def sanitize_slug(title):
    slug = title.split(':')[0].split('(')[0]
    slug = slug.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')

def call_gemini_api(title, author, description, api_key):
    prompt = f"""You are Gabriele, a Mechatronics Engineer and Technical Sales Manager.
You have read the following book:
Title: {title}
Author: {author}
Description: {description}

Please select the best category for this book from the following list of allowed categories:
{json.dumps(ALLOWED_CATEGORIES)}

Also, write a professional, personal review comment (2-3 sentences) in the first person about why you read this book and how it helps you grow, improve, or be proactive in your engineering/technical sales career or private life. Keep it inspiring, highlighting proactivity in learning.

Return your response in JSON format matching this schema:
{{
  "category": "category_name_here",
  "comment": "your_comment_here"
}}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            parsed = json.loads(text_response)
            
            category = parsed.get("category")
            if category not in ALLOWED_CATEGORIES:
                category = "My reading list"
                
            return category, parsed.get("comment", "")
    except Exception as e:
        print(f"Error calling Gemini API for '{title}': {e}")
        return None, None

def get_book_details(title, author, description):
    normalized = normalize_title(title)
    
    if normalized in PREDEFINED_BOOKS:
        print(f"-> Found predefined details for: {title}")
        return PREDEFINED_BOOKS[normalized]["category"], PREDEFINED_BOOKS[normalized]["comment"]
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print(f"-> Generating details via Gemini API for: {title}")
        category, comment = call_gemini_api(title, author, description, api_key)
        if category and comment:
            return category, comment

    print(f"-> Using fallback for: {title}")
    return "My reading list", f"I read this book to broaden my understanding and gain new perspectives. It has been a valuable addition to my reading list, supporting my continuous personal and professional development."

def download_cover_from_goodreads(image_url, slug):
    if not image_url:
        return ""
    
    filename = f"{slug}.jpg"
    filepath_local = os.path.join(STATIC_IMG_DIR, filename)
    
    # Check if local image already exists and has size > 0
    if os.path.exists(filepath_local) and os.path.getsize(filepath_local) > 0:
        return f"/images/books/{filename}"
        
    print(f"Downloading cover from Goodreads: {image_url}")
    try:
        req = urllib.request.Request(
            image_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as response:
            os.makedirs(os.path.dirname(filepath_local), exist_ok=True)
            with open(filepath_local, "wb") as f:
                f.write(response.read())
            print(f"Saved cover to: {filepath_local}")
            return f"/images/books/{filename}"
    except Exception as e:
        print(f"Failed to download cover from Goodreads: {e}")
        return ""

def fetch_book_page(book_id):
    """Cover and description from the public Goodreads book page (no sign-in needed)."""
    url = f"https://www.goodreads.com/book/show/{book_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            page = response.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Could not open the book page {url}: {e}")
        return "", ""

    def meta(prop):
        m = re.search(r'<meta[^>]+property="og:' + prop + r'"[^>]+content="([^"]*)"', page)
        return html.unescape(m.group(1)) if m else ""

    return meta("image"), meta("description")

def read_export():
    if not os.path.exists(GOODREADS_EXPORT_CSV):
        print(f"Missing {GOODREADS_EXPORT_CSV}: export your library from Goodreads and commit it there.")
        sys.exit(1)
    with open(GOODREADS_EXPORT_CSV, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def main():
    rows = read_export()
    books = [r for r in rows if (r.get("Exclusive Shelf") or "").strip() == "read"]
    print(f"Found {len(books)} read books out of {len(rows)} in the Goodreads export")
    if not books:
        print("No read books in the export: is it the right file?")
        sys.exit(1)

    os.makedirs(CONTENT_DIR, exist_ok=True)
    os.makedirs(STATIC_IMG_DIR, exist_ok=True)

    new_books_count = 0
    updated_books_count = 0

    for row in books:
        title = row["Title"].strip()
        author = row["Author"].strip()
        book_id = row["Book Id"].strip()

        slug = sanitize_slug(title)
        md_path = os.path.join(CONTENT_DIR, f"{slug}.md")
        cover_file = os.path.join(STATIC_IMG_DIR, f"{slug}.jpg")
        has_cover = os.path.exists(cover_file) and os.path.getsize(cover_file) > 0

        if os.path.exists(md_path) and has_cover:
            continue

        image_url, description = fetch_book_page(book_id)
        cover_path = download_cover_from_goodreads(image_url, slug)

        if os.path.exists(md_path):
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            frontmatter_match = re.match(r'(?s)^---\n(.*?)\n---', content)
            if frontmatter_match and "cover:" not in frontmatter_match.group(1) and cover_path:
                frontmatter = frontmatter_match.group(1)
                content = content.replace(frontmatter, frontmatter + f'\ncover: "{cover_path}"', 1)
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated cover for existing book: {title}")
                updated_books_count += 1
            continue

        print(f"New book found: {title} by {author}")
        category, comment = get_book_details(title, author, description)
        safe_title = title.replace('"', '\\"')
        markdown_content = f"""---
title: "{safe_title}"
book_authors: ["{author}"]
book_categories: ["{category}"]
link: "https://www.goodreads.com/book/show/{book_id}"
featured: false
cover: "{cover_path}"
---

{comment}
"""
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Created file: {md_path}")
        new_books_count += 1

    print(f"Done. Added {new_books_count} new books, updated {updated_books_count} existing covers.")

if __name__ == "__main__":
    main()
