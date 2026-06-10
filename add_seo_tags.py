"""
Batch script to add missing OG/Twitter meta tags to blog articles on loyueai.com.
Processes dream articles, zodiac pages, and remaining divination articles.
"""
import re
import os
import glob
from typing import Optional, Tuple, List

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))
DREAM_DIR = os.path.join(BLOG_DIR, "blog", "dream")
DIVINATION_DIR = os.path.join(BLOG_DIR, "blog", "divination")

SITE_NAME = "Tianling Pavilion"
TWITTER_CARD = "summary_large_image"
BASE_URL = "https://loyueai.com"


def extract_meta_value(content: str, prop: str) -> Optional[str]:
    """Extract value from meta tag by property name."""
    # Match <meta property="og:title" content="...">
    pattern = rf'<meta\s+property=["\']{re.escape(prop)}["\']\s+content=["\']([^"\']*)["\']'
    m = re.search(pattern, content, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def extract_name_value(content: str, name: str) -> Optional[str]:
    """Extract value from meta tag by name attribute."""
    pattern = rf'<meta\s+name=["\']{re.escape(name)}["\']\s+content=["\']([^"\']*)["\']'
    m = re.search(pattern, content, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def extract_title(content: str) -> Optional[str]:
    """Extract title from <title> tag."""
    m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    if m:
        title = m.group(1).strip()
        # Remove site suffix
        title = re.sub(r'\s*\|\s*Tianling Pavilion\s*$', '', title).strip()
        return title
    return None


def extract_canonical(content: str) -> Optional[str]:
    """Extract canonical URL."""
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']', content, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def get_image_url(filepath: str, canonical: Optional[str]) -> str:
    """Construct og:image URL from filename/canonical."""
    # Try to derive from canonical path
    if canonical:
        path = canonical.replace(BASE_URL, "")
        # Convert /blog/dream/some-name.html to /blog/images/some-name.jpg
        if "/blog/dream/" in path:
            slug = os.path.splitext(os.path.basename(path))[0]
            return f"{BASE_URL}/blog/images/{slug}.jpg"
        elif "/blog/divination/" in path:
            slug = os.path.splitext(os.path.basename(path))[0]
            return f"{BASE_URL}/blog/images/{slug}.jpg"
    # Fallback
    slug = os.path.splitext(os.path.basename(filepath))[0]
    return f"{BASE_URL}/blog/images/{slug}.jpg"


def has_full_meta(content: str) -> bool:
    """Check if file already has all required tags."""
    return bool(re.search(r'<meta\s+name=["\']twitter:card["\']', content, re.IGNORECASE))


def process_file_with_og(filepath: str) -> bool:
    """Process a file that already has og:title, og:description, og:image, og:type.
    Adds: og:url, og:site_name, twitter:card, twitter:title, twitter:description, twitter:image
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_full_meta(content):
        print(f"  SKIP (already complete): {os.path.basename(filepath)}")
        return False

    og_title = extract_meta_value(content, "og:title")
    og_desc = extract_meta_value(content, "og:description")
    og_image = extract_meta_value(content, "og:image")
    canonical = extract_canonical(content)
    og_url = canonical or get_image_url(filepath, canonical)

    if not og_title:
        print(f"  WARNING: No og:title found in {os.path.basename(filepath)}")
        return False

    # Check if ANY of the missing tags already exist
    if extract_meta_value(content, "og:url") and \
       extract_meta_value(content, "og:site_name") and \
       re.search(r'<meta\s+name=["\']twitter:card["\']', content, re.IGNORECASE):
        print(f"  SKIP (all tags present): {os.path.basename(filepath)}")
        return False

    # Build new tags
    new_tags = f'\n<meta property="og:url" content="{og_url}">\n'
    new_tags += f'<meta property="og:site_name" content="{SITE_NAME}">\n'
    new_tags += f'<meta name="twitter:card" content="{TWITTER_CARD}">\n'
    new_tags += f'<meta name="twitter:title" content="{og_title}">\n'
    new_tags += f'<meta name="twitter:description" content="{og_desc}">\n'
    new_tags += f'<meta name="twitter:image" content="{og_image}">'

    # Insert after og:type line
    # Match the og:type line and insert new tags after it
    pattern = r'(<meta\s+property=["\']og:type["\']\s+content=["\'][^"\']*["\']\s*>)'
    if not re.search(pattern, content, re.IGNORECASE):
        print(f"  WARNING: No og:type in {os.path.basename(filepath)}")
        return False

    new_content = re.sub(
        pattern,
        r'\1' + new_tags,
        content,
        count=1,
        flags=re.IGNORECASE
    )

    # Also add meta keywords if missing
    if 'meta name="keywords"' not in new_content.lower():
        title_text = extract_title(content)
        if title_text:
            kw_tag = f'\n<meta name="keywords" content="{title_text}, dream interpretation, dream meaning, Chinese dream analysis, Tianling Pavilion, free dream guide">'
            # Insert before <style> or after og:site_name
            insert_point = r'(<meta\s+name=["\']twitter:image["\']\s+content=["\'][^"\']*["\']\s*>)'
            if re.search(insert_point, new_content, re.IGNORECASE):
                new_content = re.sub(
                    insert_point,
                    r'\1' + kw_tag,
                    new_content,
                    count=1,
                    flags=re.IGNORECASE
                )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ADDED missing tags: {os.path.basename(filepath)}")
    return True


def process_file_without_og(filepath: str) -> bool:
    """Process a file that has NO og tags at all.
    Adds all OG and Twitter tags, plus keywords.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    title_text = extract_title(content)
    desc_text = extract_name_value(content, "description")
    canonical = extract_canonical(content)
    og_url = canonical or f"{BASE_URL}/blog/dream/{os.path.basename(filepath)}"
    og_image = get_image_url(filepath, canonical)

    if not title_text or not desc_text:
        print(f"  WARNING: Missing title/desc in {os.path.basename(filepath)}")
        return False

    # Build all OG + Twitter tags
    all_tags = (
        f'\n<meta property="og:title" content="{title_text}">\n'
        f'<meta property="og:description" content="{desc_text}">\n'
        f'<meta property="og:image" content="{og_image}">\n'
        f'<meta property="og:type" content="article">\n'
        f'<meta property="og:url" content="{og_url}">\n'
        f'<meta property="og:site_name" content="{SITE_NAME}">\n'
        f'<meta name="twitter:card" content="{TWITTER_CARD}">\n'
        f'<meta name="twitter:title" content="{title_text}">\n'
        f'<meta name="twitter:description" content="{desc_text}">\n'
        f'<meta name="twitter:image" content="{og_image}">\n'
        f'<meta name="keywords" content="{title_text}, dream interpretation, dream meaning, Chinese dream analysis, Tianling Pavilion, free dream guide">'
    )

    # Insert after <meta name="description" ...> tag
    pattern = r'(<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\']\s*>)'
    if not re.search(pattern, content, re.IGNORECASE):
        # Try inserting after canonical link
        pattern = r'(<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']*["\']\s*>)'
        if not re.search(pattern, content, re.IGNORECASE):
            print(f"  WARNING: No description/canonical in {os.path.basename(filepath)}")
            return False

    new_content = re.sub(
        pattern,
        r'\1' + all_tags,
        content,
        count=1,
        flags=re.IGNORECASE
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ADDED all OG+Twitter tags: {os.path.basename(filepath)}")
    return True


def process_file_with_partial_og(filepath: str) -> bool:
    """Process files that have og:title/og:desc/og:image/og:type but not the full set.
    Same as process_file_with_og but also handles files missing og:type.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_full_meta(content):
        print(f"  SKIP (already complete): {os.path.basename(filepath)}")
        return False

    has_og_type = bool(re.search(r'<meta\s+property=["\']og:type["\']', content, re.IGNORECASE))
    has_og_title = bool(re.search(r'<meta\s+property=["\']og:title["\']', content, re.IGNORECASE))

    if has_og_type and has_og_title:
        return process_file_with_og(filepath)
    elif has_og_title:
        # Has some OG but not og:type - still try to use existing values
        return process_file_with_og(filepath)
    else:
        # No OG at all
        return process_file_without_og(filepath)


def main():
    """Main processing function."""
    total_modified = 0
    total_skipped = 0

    # Phase 1: Dream articles
    print("=" * 60)
    print("PHASE 1: Processing dream articles...")
    print("=" * 60)
    dream_files = sorted(glob.glob(os.path.join(DREAM_DIR, "*.html")))
    for f in dream_files:
        if process_file_with_partial_og(f):
            total_modified += 1
        else:
            total_skipped += 1

    # Phase 2: Zodiac pages
    print("\n" + "=" * 60)
    print("PHASE 2: Processing zodiac pages...")
    print("=" * 60)
    zodiac_patterns = [
        "chinese-zodiac.html",
        "chinese-zodiac-rat.html",
        "chinese-zodiac-ox.html",
        "chinese-zodiac-tiger.html",
        "chinese-zodiac-rabbit.html",
        "chinese-zodiac-dragon.html",
        "chinese-zodiac-snake.html",
        "chinese-zodiac-horse.html",
        "chinese-zodiac-goat.html",
        "chinese-zodiac-monkey.html",
        "chinese-zodiac-rooster.html",
        "chinese-zodiac-dog.html",
        "chinese-zodiac-pig.html",
    ]
    for z in zodiac_patterns:
        f = os.path.join(DIVINATION_DIR, z)
        if os.path.exists(f):
            if process_file_with_partial_og(f):
                total_modified += 1
            else:
                total_skipped += 1

    # Phase 3: Remaining divination articles
    print("\n" + "=" * 60)
    print("PHASE 3: Processing remaining divination articles...")
    print("=" * 60)
    div_files = sorted(glob.glob(os.path.join(DIVINATION_DIR, "*.html")))
    zodiac_set = set(zodiac_patterns)
    for f in div_files:
        basename = os.path.basename(f)
        if basename in zodiac_set:
            continue  # Already processed in Phase 2
        if process_file_with_partial_og(f):
            total_modified += 1
        else:
            total_skipped += 1

    print("\n" + "=" * 60)
    print(f"SUMMARY: {total_modified} files modified, {total_skipped} files skipped")
    print("=" * 60)


if __name__ == "__main__":
    main()
