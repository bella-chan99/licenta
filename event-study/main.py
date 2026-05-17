import yfinance as yf
import pandas as pd
from pandas.tseries.offsets import BDay
from model import Model
from t_test import t_test_if_significant
from my_plots import Plot

# 1. Definim datele și indicii
important_dates = [pd.to_datetime("2022-02-24"), pd.to_datetime("2020-03-10")]

tickers_dict = {"S&P 500": "^GSPC", "Petrol Brent": "BZ=F"}

# Setările matematice pentru Event Study (Nu se schimbă)
estimation_window_days = 100
event_window_pre = 2
event_window_post = 7

# SETĂRI NOI PENTRU ZOOM OUT (Cât vedem pe grafic)
plot_window_pre = 20  # vedem 20 de zile înainte de eveniment
plot_window_post = 15  # vedem 15 zile după eveniment

for asset_name, ticker_symbol in tickers_dict.items():
    print(f"\n--- Procesare {asset_name} ({ticker_symbol}) ---")

    data = yf.download(ticker_symbol, start="2005-01-01", end="2024-01-01")["Close"]
    data = data.squeeze()  # Corecția pentru tabel

    for event_date in important_dates:
        print(f"Analizăm evenimentul din: {event_date.date()}")

        # Perioadele matematice
        estimation_start = event_date - BDay(estimation_window_days + event_window_pre)
        estimation_end = event_date - BDay(event_window_pre + 1)
        event_start = event_date - BDay(event_window_pre)
        event_end = event_date + BDay(event_window_post)

        # Perioada pentru grafic (Zoomed Out)
        plot_start = event_date - BDay(plot_window_pre)
        plot_end = event_date + BDay(plot_window_post)

        # Tăiem datele
        historical_data = data.loc[estimation_start:estimation_end]
        event_data = data.loc[event_start:event_end]
        plot_data = data.loc[plot_start:plot_end]  # Datele largi pentru plot

        if historical_data.empty or event_data.empty or plot_data.empty:
            print("  Date insuficiente pentru acest eveniment, dăm skip.")
            continue

        real_returns = event_data.pct_change().dropna()

        # Antrenăm modelul
        model = Model(historical_data)
        normal_returns = model.predict(len(real_returns))

        # Calculăm anomalia și testăm
        abnormal_returns = real_returns.values.flatten() - normal_returns
        is_sig, p_val, t_stat = t_test_if_significant(
            abnormal_returns, model.historical_std
        )
        print(f"  P-value: {p_val:.4f} -> {'SEMNIFICATIV' if is_sig else 'Zgomot'}")

        # Pasăm datele de grafic (cele lărgite) către plotter
        plotter = Plot(asset_name, event_date)
        plotter.draw_event_study(
            plot_data=plot_data,
            event_start=event_start,
            event_end=event_end,
            expected_daily_return=model.expected_daily_return,
            is_significant=is_sig,
        )
