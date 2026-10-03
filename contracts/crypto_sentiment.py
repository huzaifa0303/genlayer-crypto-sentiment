# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *


class CryptoSentimentAnalyzer(gl.Contract):

    last_coin:      str
    last_url:       str
    last_sentiment: str
    last_summary:   str
    total:          u256

    def __init__(self):
        self.last_coin      = ""
        self.last_url       = ""
        self.last_sentiment = ""
        self.last_summary   = ""
        self.total          = u256(0)

    @gl.public.write
    def analyze_coin(self, symbol: str, news_url: str) -> str:
        coin = symbol.strip().upper()
        assert len(coin) >= 1, "Symbol cannot be empty"
        assert news_url.startswith("http"), "URL must start with http"

        _coin = coin
        _url  = news_url

        def leader_fn():
            page    = gl.nondet.web.get(_url)
            content = page.body.decode("utf-8", errors="ignore")[:4000]

            prompt = f"""You are a crypto market analyst.

Coin: {_coin}
Page content from {_url}:
{content}

Is the sentiment BULLISH, BEARISH, or NEUTRAL?
Reply ONLY like this:
SENTIMENT: BULLISH
SUMMARY: one short sentence"""

            raw   = gl.nondet.exec_prompt(prompt)
            lines = raw.strip().splitlines()
            sent  = "NEUTRAL"
            note  = "No signal."

            for line in lines:
                if line.upper().startswith("SENTIMENT:"):
                    val = line.split(":", 1)[1].strip().upper()
                    if val in ("BULLISH", "BEARISH", "NEUTRAL"):
                        sent = val
                if line.upper().startswith("SUMMARY:"):
                    note = line.split(":", 1)[1].strip()[:120]

            return sent + "||" + note

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False
            try:
                v = leader_fn()
                return v.split("||")[0] == leader_result.calldata.split("||")[0]
            except Exception:
                return False

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        parts  = result.split("||", 1)

        self.last_coin      = coin
        self.last_url       = news_url
        self.last_sentiment = parts[0] if parts else "NEUTRAL"
        self.last_summary   = parts[1] if len(parts) > 1 else ""
        self.total          = u256(int(self.total) + 1)

        return self.last_sentiment

    @gl.public.view
    def get_latest(self) -> dict:
        return {
            "coin":      self.last_coin,
            "url":       self.last_url,
            "sentiment": self.last_sentiment,
            "summary":   self.last_summary,
            "total":     int(self.total),
        }

    @gl.public.view
    def get_total(self) -> int:
        return int(self.total)
