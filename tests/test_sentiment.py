"""Sentiment word-count behaviour — the lexicon is the claim, so the
counts are tested, not just the final score. Stdlib only, offline.

The report shows word counts, not just a score, and sentiment never
overrides numbers; these tests pin the counting rules that make that
claim checkable: exact-token matching, case-insensitivity, punctuation
stripping, and the score formula (pos - neg) / (pos + neg).
"""
from analyst import sentiment
from analyst.cli import DEMO


def test_demo_news_text_counts():
    # DEMO: "Strong growth and record profit beat expectations, expansion
    # continues" -> strong, growth, record, profit, beat, expansion = 6.
    # "continues" and "expectations" are not lexicon words and score 0.
    result = sentiment.sentiment_score(DEMO["news_text"])
    assert result == {"score": 1.0, "positive_words": 6,
                      "negative_words": 0, "words_scored": 6}


def test_score_formula_mixed_text():
    result = sentiment.sentiment_score("growth growth growth loss")
    assert result["positive_words"] == 3
    assert result["negative_words"] == 1
    assert result["words_scored"] == 4
    assert result["score"] == (3 - 1) / 4


def test_balanced_text_scores_zero():
    result = sentiment.sentiment_score("growth loss")
    assert result["score"] == 0.0
    assert result["words_scored"] == 2


def test_all_negative_scores_minus_one():
    result = sentiment.sentiment_score("loss decline downgrade fraud")
    assert result["score"] == -1.0
    assert result["negative_words"] == 4


def test_case_insensitive_and_punctuation_stripped():
    result = sentiment.sentiment_score("Profit! LOSS? Strong, weak.")
    assert result["positive_words"] == 2  # Profit, Strong
    assert result["negative_words"] == 2  # LOSS, weak
    assert result["score"] == 0.0


def test_repeated_words_count_each_occurrence():
    result = sentiment.sentiment_score("risk risk risk")
    assert result["negative_words"] == 3
    assert result["words_scored"] == 3


def test_exact_token_match_no_substring_credit():
    # "profitable" is not the lexicon word "profit"; only "growth" scores.
    result = sentiment.sentiment_score("profitable growth")
    assert result["positive_words"] == 1
    assert result["words_scored"] == 1


def test_unknown_words_score_nothing():
    result = sentiment.sentiment_score("the company announced Tuesday")
    assert result == {"score": 0.0, "positive_words": 0,
                      "negative_words": 0, "words_scored": 0}


def test_empty_and_none_text_are_neutral_not_errors():
    # Lenient boundary, documented not rejected: no scored words -> 0.0.
    assert sentiment.sentiment_score("")["score"] == 0.0
    assert sentiment.sentiment_score(None)["score"] == 0.0
    assert sentiment.sentiment_score(None)["words_scored"] == 0


def test_words_scored_always_equals_pos_plus_neg():
    for text in ["growth loss profit", "beat beats miss misses", ""]:
        result = sentiment.sentiment_score(text)
        assert result["words_scored"] == (
            result["positive_words"] + result["negative_words"])
