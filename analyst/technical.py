"""Technical indicators — RSI, MACD, Bollinger, SMA/EMA. Pure Python, no lookahead."""
def sma(prices, n):
    if len(prices) < n or n < 1: raise ValueError("not enough prices")
    return sum(prices[-n:]) / n
def ema(prices, n):
    if len(prices) < n: raise ValueError("not enough prices")
    k = 2 / (n + 1); e = sum(prices[:n]) / n
    for p in prices[n:]: e = p * k + e * (1 - k)
    return e
def rsi(prices, n=14):
    if len(prices) < n + 1: raise ValueError("not enough prices for RSI")
    gains = [max(prices[i]-prices[i-1], 0) for i in range(1, n+1)]
    losses = [max(prices[i-1]-prices[i], 0) for i in range(1, n+1)]
    ag, al = sum(gains)/n, sum(losses)/n
    for i in range(n+1, len(prices)):
        ag = (ag*(n-1)+max(prices[i]-prices[i-1],0))/n
        al = (al*(n-1)+max(prices[i-1]-prices[i],0))/n
    if al == 0: return 100.0
    return 100 - 100/(1+ag/al)
def macd(prices, fast=12, slow=26, signal=9):
    if len(prices) < slow: raise ValueError("not enough prices for MACD")
    def _ema_series(p, n):
        k=2/(n+1); out=[]; e=sum(p[:n])/n; out.append(e)
        for x in p[n:]: e=x*k+e*(1-k); out.append(e)
        return out
    f=_ema_series(prices, fast); s=_ema_series(prices, slow)
    offset=len(f)-len(s); line=[f[i+offset]-s[i] for i in range(len(s))]
    sig=_ema_series(line, signal) if len(line)>=signal else []
    return {"macd": line[-1], "signal": sig[-1] if sig else None, "histogram": (line[-1]-sig[-1]) if sig else None}
def bollinger(prices, n=20, k=2.0):
    if len(prices) < n: raise ValueError("not enough prices for Bollinger")
    w=prices[-n:]; m=sum(w)/n; sd=(sum((x-m)**2 for x in w)/n)**0.5
    return {"middle": m, "upper": m+k*sd, "lower": m-k*sd, "bandwidth": (2*k*sd/m) if m else 0}
