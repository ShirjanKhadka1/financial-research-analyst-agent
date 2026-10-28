"""Lexicon sentiment — deterministic, no LLM, no API. Scores news text -1..+1.
A lexicon can be wrong; that is why the report shows the word counts, not
just a score, and why sentiment never overrides numbers."""
POSITIVE={"growth","profit","record","beat","beats","strong","surge","gain","gains","expand","expansion","upgrade","outperform","robust","recovery","dividend"}
NEGATIVE={"loss","losses","miss","misses","decline","fall","falls","weak","downgrade","fraud","default","lawsuit","cut","cuts","risk","risks","scandal","bankrupt"}
def sentiment_score(text):
    words=[w.strip(".,!?:;()\"'").lower() for w in (text or "").split()]
    pos=sum(1 for w in words if w in POSITIVE); neg=sum(1 for w in words if w in NEGATIVE)
    total=pos+neg
    return {"score": (pos-neg)/total if total else 0.0, "positive_words": pos, "negative_words": neg, "words_scored": total}
