# CryptoSentimentAnalyzer — GenLayer Intelligent Contract

An Intelligent Contract deployed on **GenLayer Testnet Bradbury** that
fetches live crypto news and uses an LLM to determine market sentiment
(**BULLISH / BEARISH / NEUTRAL**) fully on-chain — no oracles needed.

## What it does

1. Fetches a live crypto news page (CoinDesk, CryptoPanic, etc.)
2. Asks an LLM to judge sentiment for any coin symbol
3. Reaches consensus via **Optimistic Democracy**
4. Stores the result on-chain

## Contract Methods

| Method | Type | Description |
|---|---|---|
| `analyze_coin(symbol, news_url)` | write | Fetches news, runs LLM, returns sentiment |
| `get_latest()` | view | Returns the most recent analysis |
| `get_total()` | view | Total number of analyses done |

## Deployment

- **Network:** GenLayer Testnet Bradbury
- **Contract address:** `0x5EfEdDCAf809C0C282a738cf1a52070846020281`
- **Deploy tx:** `0xb3cc...`

## Example Usage
