# API Documentation

## Run Analysis (Main Function)

`run_analysis_for_ticker(self, fund: str) -> Tuple[VFStopsResultType, bool]`

**fund: str** - Fund ticker symbol (e.g. "SPY")

## Returned Data (Captured from `yfinance`)

`return_data(self, fund="", key: Union[str, None] = None) -> Union[dict, list]`

Returns the full ticker data as a dict or a list, if supplied the ticker data object key.

**fund: str = ""**

**key: Union[str, None] = None**

| `fund` | `key` | Returned Data |
| --- | ---- | ---------- |
| `""` / `None` | don't care | All data (list of all funds data) |
| provided | None | Fund data of 'Close' |
| provided | one of [`'Close'`, `'Open'`, `'High'`, `'Low'`] | Fund data of supplied key |
| provided | `'__full__'` | all of single fund data |