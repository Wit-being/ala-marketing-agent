import os
import re
import random
from datetime import datetime, timezone
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ── Topic pool — varied, SEO-friendly dream topics ───────────────────────────
TOPICS = [
    {"title": "Why You Forget Your Dreams Within Minutes of Waking Up", "keyword": "why do we forget dreams"},
    {"title": "What It Means When You Dream About Someone You Haven't Seen in Years", "keyword": "dreaming about someone"},
    {"title": "The Science Behind Lucid Dreaming and How It Actually Works", "keyword": "lucid dreaming science"},
    {"title": "Why Some People Never Dream and What That Says About Sleep", "keyword": "people who don't dream"},
    {"title": "What Nightmares Are Actually Trying to Tell You", "keyword": "what do nightmares mean"},
    {"title": "The Connection Between Stress and Vivid Dreams", "keyword": "stress and vivid dreams"},
    {"title": "Why We Dream in Symbols and What They Actually Mean", "keyword": "dream symbols meaning"},
    {"title": "What Happens in Your Brain While You Dream", "keyword": "what happens in brain during dreams"},
    {"title": "Why Recurring Dreams Happen and How to Stop Them", "keyword": "why do I keep having the same dream"},
    {"title": "The Difference Between REM Sleep and Deep Sleep Dreams", "keyword": "REM sleep dreams"},
    {"title": "Why Your Dreams Feel So Real Sometimes", "keyword": "why do dreams feel real"},
    {"title": "What Falling Dreams Mean According to Sleep Science", "keyword": "falling dreams meaning"},
    {"title": "Can Dreams Help You Solve Real Problems? What Research Says", "keyword": "dreams problem solving"},
    {"title": "Why We Dream About Death and What It Actually Means", "keyword": "dreaming about death meaning"},
    {"title": "The Psychology of Being Chased in Dreams", "keyword": "being chased in dreams meaning"},
]

topic = random.choice(TOPICS)
title = topic["title"]
keyword = topic["keyword"]

# ── Generate blog post content ────────────────────────────────────────────────
prompt = f"""Write a compelling, human-sounding blog post for Àlá, a dream journaling and sharing app at alaapp.site.

Title: {title}
Focus keyword: {keyword}

Requirements:
- 600 to 800 words
- Written in first or second person, conversational and warm, not clinical
- Uses the focus keyword naturally in the first paragraph and 2-3 times throughout
- Has 3 to 4 subheadings using ## markdown
- Ends with a soft, natural mention of Àlá and a link to alaapp.site — not a hard sell, just a natural sign-off
- No bullet point lists — flowing prose only
- No emojis
- Sounds like a real person wrote it, not a content mill

Write only the blog post body content. No title, no frontmatter, just the body text starting from the first paragraph.
"""

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1200,
    temperature=0.85,
)

content = completion.choices[0].message.content.strip()

# ── Generate excerpt ──────────────────────────────────────────────────────────
excerpt_prompt = f"Write a single sentence excerpt (max 160 characters) for a blog post titled: '{title}'. Make it compelling and click-worthy. Reply with only the excerpt text."

excerpt_completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": excerpt_prompt}],
    max_tokens=60,
    temperature=0.7,
)

excerpt = excerpt_completion.choices[0].message.content.strip().strip('"')
if len(excerpt) > 160:
    excerpt = excerpt[:157] + "..."

# ── Build slug from title ─────────────────────────────────────────────────────
slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

# ── Build frontmatter ─────────────────────────────────────────────────────────
date = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')

frontmatter = f"""---
title: "{title}"
excerpt: "{excerpt}"
date: "{date}"
author: "Àlá Team"
tags:

coverImage: ""
seo:
  metaDescription: "{excerpt}"
  focusKeyword: "{keyword}"
---

"""

# ── Write file ────────────────────────────────────────────────────────────────
filename = f"ala-website/content/blog/{slug}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(frontmatter + content)

print(f"Blog post written: {filename}")
print(f"Title: {title}")
print(f"Keyword: {keyword}")
print(f"Excerpt: {excerpt}")
