"""NYT headline sentiment scorer with phrase-level awareness.

Parses NYT RSS feeds and scores headlines on four axes (negative, positive,
uncertainty, oil-relevance). Phrases outweigh individual words so that
"end the war" does not score the same as "start the war".
"""

import re
from collections import Counter
import feedparser

NEGATIVE_WORDS = ('war attack attacked strike strikes struck bomb bombed bombing missile missiles drone sanctions '
    'blockade closure closed threat threatens threatened escalation escalate conflict crisis retaliation '
    'retaliatory destroy destroyed destruction casualties killed dead invasion invaded military nuclear weapon '
    'weapons hostile hostilities siege shelling fired intercepted violated').split()
POSITIVE_WORDS = ('ceasefire peace deal agreement treaty reopening reopened opened diplomatic diplomacy truce '
    'negotiations negotiate easing eased lifted resolved resolution cooperation deescalation withdrawal '
    'humanitarian aid stabilize stabilized recovery restored').split()
UNCERTAINTY_WORDS = ('unclear uncertain uncertainty disputed volatile volatility unstable tensions risk warns '
    'warning feared fears anxiety unpredictable contested fragile precarious doubt doubts stalemate impasse '
    'brink turmoil chaos').split()
OIL_WORDS = ['oil', 'crude', 'petroleum', 'barrel', 'barrels', 'opec', 'refinery', 'pipeline', 'tanker',
    'tankers', 'shipping', 'strait', 'hormuz', 'energy', 'fuel', 'gasoline', 'lng', 'natural gas', 'supply',
    'supplies', 'export', 'imports']
POSITIVE_PHRASES = [
    'end war', 'end the war', 'ending the war', 'ends war', 'stop war', 'stop the war', 'peace deal',
    'peace agreement', 'peace talks', 'peace process', 'ceasefire holds', 'ceasefire holding', 'truce holds',
    'open strait', 'reopen strait', 'reopened strait', 'reopening strait', 'strait reopened', 'strait open',
    'hormuz open', 'hormuz reopened', 'lift sanctions', 'lifting sanctions', 'sanctions lifted', 'lift blockade',
    'lifting blockade', 'blockade lifted', 'ease tensions', 'easing tensions', 'tensions ease', 'deescalation',
    'de-escalation', 'war ends', 'conflict ends', 'withdraw troops', 'withdrawal complete', 'aid delivered',
    'humanitarian corridor', 'diplomatic breakthrough', 'deal reached', 'agreement reached', 'accord signed',
    'normalize relations', 'talks resume', 'talks progress']
NEGATIVE_PHRASES = [
    'start war', 'declare war', 'new war', 'escalate war', 'close strait', 'closed strait', 'closing strait',
    'strait closed', 'hormuz closed', 'hormuz closure', 'attack ships', 'attacked ships', 'ships attacked',
    'fire missiles', 'fired missiles', 'launch missiles', 'nuclear threat', 'nuclear weapon', 'nuclear program',
    'oil shock', 'supply disruption', 'supply crisis', 'blockade imposed', 'impose blockade', 'new sanctions',
    'impose sanctions', 'troops deployed', 'military buildup', 'invasion begins', 'ground offensive',
    'aerial bombardment', 'civilian casualties', 'mass casualties', 'chemical weapons', 'break ceasefire',
    'ceasefire broken', 'ceasefire violated', 'ceasefire collapses', 'truce broken', 'talks collapse',
    'talks fail', 'negotiations fail', 'deal collapses', 'threatens retaliation', 'vows retaliation']
DEFAULT_FEEDS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml",
]

_NEG = set(NEGATIVE_WORDS); _POS = set(POSITIVE_WORDS); _UNC = set(UNCERTAINTY_WORDS)
_OIL_SINGLE = {w for w in OIL_WORDS if ' ' not in w}
_OIL_MULTI = [w for w in OIL_WORDS if ' ' in w]


def _tokenize(text):
    """Return lowercase alphanumeric tokens."""
    return re.findall(r"[a-z0-9]+", text.lower())


def _phrase_pattern(phrase, max_gap=2):
    """Compile a regex matching `phrase` with prefix tolerance per token and
    up to `max_gap` intervening words (so 'end war' matches 'end the iran war')."""
    tokens = phrase.split()
    parts = [re.escape(t) + r'\w*' for t in tokens]
    if len(tokens) == 1:
        return re.compile(r'\b' + parts[0] + r'\b', re.IGNORECASE)
    sep = r'\s+(?:\w+\s+){0,' + str(max_gap) + r'}'
    return re.compile(r'\b' + sep.join(parts) + r'\b', re.IGNORECASE)


_POS_PATTERNS = [(p, _phrase_pattern(p)) for p in sorted(POSITIVE_PHRASES, key=len, reverse=True)]
_NEG_PATTERNS = [(p, _phrase_pattern(p)) for p in sorted(NEGATIVE_PHRASES, key=len, reverse=True)]
_PATTERN_MAP = dict(_POS_PATTERNS + _NEG_PATTERNS)


def score_headline(text):
    """Score one headline with phrase + word awareness. Phrases (weight 2) match
    first and are removed before single-word scoring runs on the residual.
    Returns negative_count, positive_count, uncertainty_count, oil_related,
    net_sentiment, risk_score, matched_positive_phrases, matched_negative_phrases."""
    original = (text or "").lower()
    residual = original
    matched_pos, matched_neg = [], []
    pos_ct = neg_ct = 0
    for phrase, pat in _POS_PATTERNS:
        residual, n = pat.subn(" ", residual)
        if n:
            matched_pos.append(phrase); pos_ct += 2 * n
    for phrase, pat in _NEG_PATTERNS:
        residual, n = pat.subn(" ", residual)
        if n:
            matched_neg.append(phrase); neg_ct += 2 * n
    rc = Counter(_tokenize(residual))
    neg_ct += sum(c for t, c in rc.items() if t in _NEG)
    pos_ct += sum(c for t, c in rc.items() if t in _POS)
    unc_ct = sum(c for t, c in rc.items() if t in _UNC)
    oc = Counter(_tokenize(original))
    oil = any(t in _OIL_SINGLE for t in oc) or any(p in original for p in _OIL_MULTI)
    return {"negative_count": neg_ct, "positive_count": pos_ct, "uncertainty_count": unc_ct,
            "oil_related": oil, "net_sentiment": pos_ct - neg_ct, "risk_score": neg_ct + unc_ct,
            "matched_positive_phrases": matched_pos, "matched_negative_phrases": matched_neg}


def fetch_nyt_headlines(feeds=None):
    """Fetch, dedupe, and score NYT RSS headlines. Newest-first. Per-feed
    network errors yield an empty contribution for that feed."""
    feeds = feeds or DEFAULT_FEEDS
    seen, out = set(), []
    for url in feeds:
        try:
            parsed = feedparser.parse(url)
        except Exception:
            continue
        for entry in parsed.get("entries", []):
            title = (entry.get("title") or "").strip()
            if not title or title in seen:
                continue
            seen.add(title)
            desc = re.sub(r"<[^>]+>", "", entry.get("summary") or entry.get("description") or "").strip()
            tags = entry.get("tags") or []
            cats = [t.get("term", "") for t in tags if isinstance(t, dict)]
            out.append({"title": title, "description": desc,
                        "published": entry.get("published") or entry.get("updated") or "",
                        "categories": cats,
                        "sentiment": score_headline(f"{title}. {desc}")})
    out.sort(key=lambda h: h["published"] or "", reverse=True)
    return out


def compute_daily_sentiment(headlines):
    """Aggregate scored headlines. Returns total_headlines, avg_risk_score,
    avg_net_sentiment, oil_related_pct, escalation_pct, deescalation_pct,
    headline_gpr_proxy (= 100 + avg_risk_score * 50), top_risk_headline, signal."""
    n = len(headlines)
    if n == 0:
        return {"total_headlines": 0, "avg_risk_score": 0.0, "avg_net_sentiment": 0.0,
                "oil_related_pct": 0.0, "escalation_pct": 0.0, "deescalation_pct": 0.0,
                "headline_gpr_proxy": 100.0, "top_risk_headline": None, "signal": "LOW"}
    ss = [h["sentiment"] for h in headlines]
    avg_risk = sum(s["risk_score"] for s in ss) / n
    avg_net = sum(s["net_sentiment"] for s in ss) / n
    oil_pct = 100.0 * sum(1 for s in ss if s["oil_related"]) / n
    esc = 100.0 * sum(1 for s in ss if s["matched_negative_phrases"]) / n
    de = 100.0 * sum(1 for s in ss if s["matched_positive_phrases"]) / n
    top = max(headlines, key=lambda h: h["sentiment"]["risk_score"])
    signal = "ELEVATED RISK" if avg_risk > 2.0 else "MODERATE" if avg_risk > 1.0 else "LOW"
    return {"total_headlines": n, "avg_risk_score": avg_risk, "avg_net_sentiment": avg_net,
            "oil_related_pct": oil_pct, "escalation_pct": esc, "deescalation_pct": de,
            "headline_gpr_proxy": 100.0 + avg_risk * 50.0,
            "top_risk_headline": top, "signal": signal}


def format_headline_html(headline_dict):
    """Render one headline as HTML with color coding and bolded matched phrases
    (green positive, red negative)."""
    s = headline_dict["sentiment"]
    bg = ("#f8d7da" if s["risk_score"] >= 3 else "#ffe5b4" if s["risk_score"] >= 1
          else "#d4edda" if s["net_sentiment"] > 0 else "#e9ecef")
    title = headline_dict.get("title", "").replace("<", "&lt;").replace(">", "&gt;")
    for p in s.get("matched_positive_phrases", []):
        pat = _PATTERN_MAP.get(p)
        if pat:
            title = pat.sub(lambda m: f'<b style="color:#1f7a1f">{m.group(0)}</b>', title)
    for p in s.get("matched_negative_phrases", []):
        pat = _PATTERN_MAP.get(p)
        if pat:
            title = pat.sub(lambda m: f'<b style="color:#a02020">{m.group(0)}</b>', title)
    return (f'<div style="background:{bg};padding:8px;margin:4px 0;border-radius:4px;'
            f'font-family:sans-serif"><div style="font-weight:600">{title}</div>'
            f'<div style="font-size:11px;color:#555">{headline_dict.get("published","")}</div>'
            f'<div style="font-size:11px;color:#333">neg={s["negative_count"]} '
            f'pos={s["positive_count"]} unc={s["uncertainty_count"]} '
            f'oil={"Y" if s["oil_related"] else "N"}</div></div>')


if __name__ == "__main__":
    test_headlines = [
        "How the War Powers Act Could Pressure Trump to End the Iran War",
        "Iran Closes Strait of Hormuz Again Over US Blockade",
        "Peace Deal Reached Between US and Iran on Nuclear Program",
        "Ships Attacked in Strait of Hormuz as Iran Declares Control",
        "Ceasefire Holds as Displaced Lebanese Head Home",
    ]
    print("=== Phrase-Aware Scoring Tests ===")
    for t in test_headlines:
        r = score_headline(t)
        matched = r["matched_positive_phrases"] + [f"-{p}" for p in r["matched_negative_phrases"]]
        print(f"risk={r['risk_score']:<2} net={r['net_sentiment']:<+3} | {t}\n  matched: {matched}")

    headlines = fetch_nyt_headlines()
    s = compute_daily_sentiment(headlines)
    print(f"\nFetched {len(headlines)} headlines.\n=== Daily Sentiment Summary ===")
    print(f"Signal: {s['signal']} | Avg risk/net: {s['avg_risk_score']:.2f}/{s['avg_net_sentiment']:+.2f}")
    print(f"Oil%: {s['oil_related_pct']:.1f} | Esc%: {s['escalation_pct']:.1f} | De%: {s['deescalation_pct']:.1f}")
    print(f"Headline GPR proxy: {s['headline_gpr_proxy']:.1f}")
    if s["top_risk_headline"]:
        tr = s["top_risk_headline"]; print(f"Top risk: [{tr['sentiment']['risk_score']}] {tr['title']}")
    print("\n=== Top 5 by risk_score ===")
    for i, h in enumerate(sorted(headlines, key=lambda x: x["sentiment"]["risk_score"], reverse=True)[:5], 1):
        v = h["sentiment"]; print(f"{i}. [risk={v['risk_score']} net={v['net_sentiment']:+d} oil={'Y' if v['oil_related'] else 'N'}] {h['title']}")
