import json

import yfinance as yf

try:
    import pandas as pd
except ImportError:  # pragma: no cover - yfinance pulls pandas in practice
    pd = None


def to_jsonable(data):
    if pd is not None:
        if isinstance(data, pd.DataFrame):
            return json.loads(data.to_json(orient="split", date_format="iso"))
        if isinstance(data, pd.Series):
            return json.loads(data.to_json(date_format="iso"))

    if isinstance(data, dict):
        return {str(key): to_jsonable(value) for key, value in data.items()}

    if isinstance(data, (list, tuple, set)):
        return [to_jsonable(value) for value in data]

    if hasattr(data, "isoformat"):
        try:
            return data.isoformat()
        except TypeError:
            pass

    if hasattr(data, "item"):
        try:
            return data.item()
        except Exception:
            pass

    return data


def write_to_file(filename, data):
    with open("yahoo-finance-outputs/" + filename, "w") as f:
        json.dump(to_jsonable(data), f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    dat = yf.Ticker("TLV.RO")
    write_to_file("info.jsonc", dat.info)
    write_to_file("calendar.jsonc", dat.calendar)
    write_to_file("analyst_price_targets.jsonc", dat.analyst_price_targets)
    write_to_file("quarterly_income_stmt.jsonc", dat.quarterly_income_stmt)
    write_to_file("history.jsonc", dat.history(period="1mo"))
    if dat.options:
        write_to_file("option_chain.jsonc", dat.option_chain(dat.options[0]).calls)
    else:
        print("Skipping option_chain.jsonc: ticker has no options")


if __name__ == "__main__":
    main()
