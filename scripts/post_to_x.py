import os
import tweepy
import urllib.request
import json
import random

# ── Groq API setup (free, no billing needed) ─────────────────────────────────
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ── Tweet prompt variations ───────────────────────────────────────────────────
PROMPTS = [
    "Write a single tweet (max 260 characters) for @alaapp_, a dream journaling and sharing app. The tweet should be thought-provoking, mysterious or fascinating about dreams. No hashtags. No emojis unless they add value. Conversational, not corporate. Don't mention the app directly. Reply with only the tweet text, nothing else.",
    "Write a single tweet (max 260 characters) for @alaapp_. Ask a curious question about dreams that makes people stop and think. Something that non-dreamers and vivid dreamers alike would find interesting. No hashtags. Reply with only the tweet text, nothing else.",
    "Write a single tweet (max 260 characters) for @alaapp_. Share a surprising or little-known fact about dreams or sleep. Make it feel like something you'd text a friend, not a press release. No hashtags. Reply with only the tweet text, nothing else.",
    "Write a single tweet (max 260 characters) for @alaapp_. Write something poetic but grounded about the feeling of forgetting a dream right after waking up. Relatable, not cheesy. No hashtags. Reply with only the tweet text, nothing else.",
    "Write a single tweet (max 260 characters) for @alaapp_. Write something about the experience of having a dream so vivid it stays with you all day. Short, punchy, conversational. No hashtags. Reply with only the tweet text, nothing else.",
    "Write a single tweet (max 260 characters) for @alaapp_. Share something interesting about the connection between emotions and dreaming. Accessible, curious tone. No hashtags. Reply with only the tweet text, nothing else.",
    "Write a single tweet (max 260 characters) for @alaapp_. Write a tweet about what it would mean if you could read someone else's dream. Thought-provoking, not promotional. No hashtags. Reply with only the tweet text, nothing else.",
]

# ── Generate tweet content via Groq ──────────────────────────────────────────
prompt = random.choice(PROMPTS)

payload = json.dumps({
    "model": "llama3-8b-8192",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 100,
    "temperature": 0.9,
}).encode("utf-8")

req = urllib.request.Request(
    GROQ_URL,
    data=payload,
    headers={
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "ala-marketing-agent/1.0",
    },
    method="POST",
)

with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode("utf-8"))

tweet_text = data["choices"][0]["message"]["content"].strip()

# Clean up any quotation marks the model wraps around the tweet
if tweet_text.startswith('"') and tweet_text.endswith('"'):
    tweet_text = tweet_text[1:-1].strip()

# Safety check
if len(tweet_text) > 280:
    tweet_text = tweet_text[:277] + "..."

print(f"Generated tweet ({len(tweet_text)} chars):\n{tweet_text}\n")

# ── Post to X via OAuth 1.0a ──────────────────────────────────────────────────
client_x = tweepy.Client(
    consumer_key=os.environ["X_API_KEY"],
    consumer_secret=os.environ["X_API_SECRET"],
    access_token=os.environ["X_ACCESS_TOKEN"],
    access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
)

response_x = client_x.create_tweet(text=tweet_text)
print(f"Tweet posted successfully. Tweet ID: {response_x.data['id']}")
