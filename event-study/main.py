import yfinance as yf
import pandas as pd
from pandas.tseries.offsets import BDay
from model import Model
from t_test import t_test_if_significant
from my_plots import Plot

# 1. Definim datele și indicii
# Format YYYY-MM-DD. Ex: 24 Feb 2022 = Ucraina, 15 Sep 2008 = Lehman Brothers
important_dates = [pd.to_datetime("2022-02-24"), pd.to_datetime("2020-03-10")]

# Tickere reale din Yahoo Finance. "^BEst" e un proxy pt BET sau putem lua acțiuni mari, "BZ=F" e Petrolul Brent, "^STOXX50E" e Euro Stoxx 50.
tickers_dict = {"S&P 500": "^GSPC", "Petrol Brent": "BZ=F"}

# 2. Setările pentru Event Study
estimation_window_days = (
    100  # Ne uităm la 100 de zile în spate pentru a antrena modelul
)
event_window_pre = 2  # Ne uităm cu 2 zile înainte (pentru zvonuri)
event_window_post = 7  # Ne uităm la 7 zile după (pentru reacție/underreaction)

for asset_name, ticker_symbol in tickers_dict.items():
    print(f"\n--- Procesare {asset_name} ({ticker_symbol}) ---")

    # Descărcăm istoric masiv ca să avem de unde tăia (ultimii 20 de ani)
    # În viața reală s-ar putea să vrei să salvezi datele într-un CSV ca să nu faci call-uri pe net la fiecare rulare
    data = yf.download(ticker_symbol, start="2005-01-01", end="2024-01-01")["Close"]

    for event_date in important_dates:
        print(f"Analizăm evenimentul din: {event_date.date()}")

        # Calculăm exact ferestrele folosind Business Days (sărim weekendurile)
        estimation_start = event_date - BDay(estimation_window_days + event_window_pre)
        estimation_end = event_date - BDay(event_window_pre + 1)

        event_start = event_date - BDay(event_window_pre)
        event_end = event_date + BDay(event_window_post)

        # Tăiem datele (slice)
        historical_data = data.loc[estimation_start:estimation_end]
        event_data = data.loc[event_start:event_end]

        # Dacă nu avem date pentru perioada respectivă (ex: sărbătoare legală sau lipsă date), dăm skip
        if historical_data.empty or event_data.empty:
            print("  Date insuficiente pentru acest eveniment, dăm skip.")
            continue

        # Transformăm prețurile din fereastra de eveniment în randamente reale
        real_returns = event_data.pct_change().dropna()
        event_dates_index = real_returns.index

        # Inițializăm și "antrenăm" modelul
        model = Model(historical_data)

        # Prezicem randamentul normal (baseline-ul)
        normal_returns = model.predict(len(real_returns))

        # Calculăm diferența (Randamentul Anormal - AR)
        abnormal_returns = real_returns.values.flatten() - normal_returns

        # Testăm dacă panica e semnificativă
        is_sig, p_val, t_stat = t_test_if_significant(
            abnormal_returns, model.historical_std
        )
        print(f"  P-value: {p_val:.4f} -> {'SEMNIFICATIV' if is_sig else 'Zgomot'}")

        # Desenăm graficul
        plotter = Plot(asset_name, event_date)
        plotter.draw_event_study(
            event_dates_index, real_returns.values.flatten(), normal_returns, is_sig
        )

