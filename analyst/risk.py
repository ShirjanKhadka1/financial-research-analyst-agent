"""Risk: historical VaR/CVaR, drawdown, beta, Monte Carlo VaR. Seeded, reproducible."""
import math
import random


def returns_from_prices(prices):
    if len(prices)<2: raise ValueError("need at least 2 prices")
    return [prices[i]/prices[i-1]-1 for i in range(1,len(prices)) if prices[i-1]!=0]
def historical_var(returns, alpha=0.05):
    s=sorted(returns); k=max(0,math.floor(alpha*len(s))); return -s[k]
def historical_cvar(returns, alpha=0.05):
    s=sorted(returns); k=max(1,math.floor(alpha*len(s))); return -sum(s[:k])/k
def max_drawdown(prices):
    peak=prices[0]; worst=0.0
    for p in prices:
        peak=max(peak,p); worst=min(worst, p/peak-1)
    return worst
def beta(asset_returns, market_returns):
    if len(asset_returns)!=len(market_returns) or len(asset_returns)<2: raise ValueError("beta needs equal, >=2 returns")
    ma=sum(market_returns)/len(market_returns); aa=sum(asset_returns)/len(asset_returns)
    num=sum((m-ma)*(a-aa) for m,a in zip(market_returns,asset_returns))
    den=sum((m-ma)**2 for m in market_returns)
    return num/den if den else None
def monte_carlo_var(S0, mu, sigma, days=10, n_paths=10000, alpha=0.05, seed=42):
    rng=random.Random(seed); ends=[]
    for _ in range(n_paths):
        p=S0
        for _ in range(days): p*=math.exp((mu-0.5*sigma*sigma)/252 + sigma*math.sqrt(1/252)*rng.gauss(0,1))
        ends.append(p/S0-1)
    return historical_var(ends, alpha)
