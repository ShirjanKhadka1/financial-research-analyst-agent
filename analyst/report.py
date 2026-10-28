"""Markdown report generator — one page, every number traced to its agent."""
def _bullets(items):
    return [f"- {x}" for x in items] if items else ["- (none)"]
def render(result, title="Company Research Report"):
    v = result["valuation"]; d = result["debate"]
    lines = [f"# {title}", "",
             f"**As of:** {result['as_of']} | **Company type:** {result['company_type']} | **Audit chain valid:** {result['audit_valid']} ({result['audit_entries']} entries)",
             "", "## Verdict", "", f"**{d['verdict']}**",
             "", "### Bull"] + _bullets(d["bull"]) + ["", "### Bear"] + _bullets(d["bear"]) + [
             "", "## Valuation", "", f"Blended value: {v['blended_value']} | Gap vs price: {v['gap_vs_price']}",
             "", "## Risk", "", f"VaR (5%): {result['risk']['var_5pct']:.4f} | CVaR (5%): {result['risk']['cvar_5pct']:.4f} | Max drawdown: {result['risk']['max_drawdown']:.4f} | Beta: {result['risk']['beta']}",
             "", "## Fundamentals", "", f"Piotroski: {result['piotroski']['score']}/9 | Ratios: {result['fundamental_ratios']}",
             "", "## Sentiment (lexicon, not LLM)", "", f"{result['sentiment']}",
             "", "## Falsifier", "", result["falsifier"],
             "", f"*{result['disclaimer']}*"]
    return "\n".join(lines)
