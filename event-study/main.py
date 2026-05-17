import yfinance as yf
import pandas as pd
from pandas.tseries.offsets import BDay
from model import Model
from t_test import t_test_if_significant
from my_plots import Plot

# 1. Mapăm datele la tag-uri clare cu numele evenimentelor
important_events = {
    pd.to_datetime("2008-09-15"): "Criza Financiară Globală (Lehman Brothers)",
    pd.to_datetime("2020-03-10"): "Pandemia COVID-19 (Crahul Bursier)",
    pd.to_datetime("2022-02-24"): "Războiul din Ucraina (Șoc Geopolitic)",
}

# 2. Configurația de active conform mixului tău structural din licență
# Am adăugat Euro Stoxx 50 și proxy-ul pentru BET (Banca Transilvania)
tickers_dict = {
    "S&P 500": "^GSPC",
    "Euro Stoxx 50 (Piețe Mature)": "^STOXX50E",
    "Petrol Brent (Canal Energetic)": "BZ=F",
    "Indicele BET (Proxy: TLV.RO)": "TLV.RO",
}

# Setările matematice pentru Event Study
estimation_window_days = 100
event_window_pre = 2
event_window_post = 7

# Setări pentru Zoom Out pe grafice
plot_window_pre = 20
plot_window_post = 15

for asset_name, ticker_symbol in tickers_dict.items():
    print(f"\n--- Procesare {asset_name} ({ticker_symbol}) ---")

    # Descărcare implicită din Yahoo Finance
    data = yf.download(ticker_symbol, start="2005-01-01", end="2026-01-01")["Close"]
    data = data.squeeze()

    # --- BONUS ACADEMIC: CODUL PENTRU FIȘIERUL REAL DE LA BVB ---
    # Dacă descarci manual istoricul BET sub formă de CSV, numește-l 'BET.csv' și decomentează liniile de mai jos:
    # if "BET" in asset_name:
    #     try:
    #         df_bet = pd.read_csv("BET.csv", parse_dates=['Data'], index_col='Data')
    #         data = df_bet['Valoare'].squeeze()
    #         asset_name = "Indicele BET (Date Oficiale BVB)"
    #     except FileNotFoundError:
    #         print("  [Info] Nu s-a găsit BET.csv local. Rulăm automat pe proxy-ul TLV.RO de pe Yahoo Finance.")

    for event_date, event_name in important_events.items():
        print(f"Analizăm: {event_name} | Data: {event_date.date()}")

        # Calculare ferestre temporale
        estimation_start = event_date - BDay(estimation_window_days + event_window_pre)
        estimation_end = event_date - BDay(event_window_pre + 1)
        event_start = event_date - BDay(event_window_pre)
        event_end = event_date + BDay(event_window_post)

        plot_start = event_date - BDay(plot_window_pre)
        plot_end = event_date + BDay(plot_window_post)

        # Tăiere date (Slicing)
        historical_data = data.loc[estimation_start:estimation_end]
        event_data = data.loc[event_start:event_end]
        plot_data = data.loc[plot_start:plot_end]

        if historical_data.empty or event_data.empty or plot_data.empty:
            print(f"  Date insuficiente pentru '{event_name}', dăm skip.")
            continue

        real_returns = event_data.pct_change().dropna()

        # Rulare Model Economic
        model = Model(historical_data)
        normal_returns = model.predict(len(real_returns))

        # Evaluare anomalie și T-Test
        abnormal_returns = real_returns.values.flatten() - normal_returns
        is_sig, p_val, t_stat = t_test_if_significant(
            abnormal_returns, model.historical_std
        )
        print(f"  P-value: {p_val:.4f} -> {'SEMNIFICATIV' if is_sig else 'Zgomot'}")

        # Generare plot dublu cu titlu customizat per eveniment
        plotter = Plot(asset_name, event_date, event_name)
        plotter.draw_event_study(
            plot_data=plot_data,
            event_start=event_start,
            event_end=event_end,
            expected_daily_return=model.expected_daily_return,
            is_significant=is_sig,
        )
