"""CompanyProfile — fundamental data for any ticker.

Pulls income statement, balance sheet, valuation, earnings from yfinance.

Usage:
    from company_profile import CompanyProfile
    profile = CompanyProfile("AAPL")
    print(profile.summary())
    print(profile.financials())
"""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Any, Dict
sys.path.insert(0, str(Path(__file__).parent))

class CompanyProfile:
    def __init__(self, symbol: str):
        import yfinance as yf
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)
        self._info = None

    @property
    def info(self):
        if self._info is None:
            self._info = self.ticker.info or {}
        return self._info

    def summary(self) -> Dict[str, Any]:
        i = self.info
        return {
            "symbol": self.symbol, "name": i.get("longName", ""),
            "sector": i.get("sector", ""), "industry": i.get("industry", ""),
            "market_cap": i.get("marketCap"), "pe_ratio": i.get("trailingPE"),
            "forward_pe": i.get("forwardPE"), "pb_ratio": i.get("priceToBook"),
            "dividend_yield": i.get("dividendYield"),
            "beta": i.get("beta"), "52w_high": i.get("fiftyTwoWeekHigh"),
            "52w_low": i.get("fiftyTwoWeekLow"),
            "avg_volume": i.get("averageVolume"),
            "revenue": i.get("totalRevenue"), "profit_margin": i.get("profitMargins"),
            "roe": i.get("returnOnEquity"), "debt_to_equity": i.get("debtToEquity"),
            "free_cash_flow": i.get("freeCashflow"),
            "tradingview": f"https://www.tradingview.com/chart/?symbol={self.symbol}",
            "yahoo": f"https://finance.yahoo.com/quote/{self.symbol}/",
        }

    def financials(self) -> Dict[str, Any]:
        try:
            inc = self.ticker.quarterly_income_stmt
            bal = self.ticker.quarterly_balance_sheet
            return {
                "income_statement": inc.to_dict() if inc is not None and not inc.empty else {},
                "balance_sheet": bal.to_dict() if bal is not None and not bal.empty else {},
            }
        except: return {}

    def earnings(self) -> Dict[str, Any]:
        try:
            e = self.ticker.quarterly_earnings
            return {"quarterly_earnings": e.to_dict() if e is not None and not e.empty else {}}
        except: return {}

    def analyst_recs(self) -> Dict[str, Any]:
        try:
            r = self.ticker.recommendations
            if r is not None and not r.empty:
                return {"recommendations": r.tail(10).to_dict()}
        except: pass
        return {}

if __name__ == "__main__":
    import json, sys
    sym = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    p = CompanyProfile(sym)
    print(json.dumps(p.summary(), indent=2, default=str))
