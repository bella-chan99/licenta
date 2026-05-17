import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Plot:
    def __init__(self, ticker_name, event_date, event_name):
        self.ticker_name = ticker_name
        self.event_date = pd.to_datetime(event_date)
        self.event_name = event_name

    def draw_event_study(
        self, plot_data, event_start, event_end, expected_daily_return, is_significant
    ):
        """
        Desenează 2 grafice: Variațiile zilnice și Prăbușirea valorii din Fereastra de Eveniment.
        """
        plot_returns = plot_data.pct_change().dropna()

        # Evoluția banilor (Start de la 100 unități monetare)
        real_cumulative = (1 + plot_returns).cumprod() * 100

        expected_returns_array = np.repeat(expected_daily_return, len(plot_returns))
        expected_cumulative = (1 + expected_returns_array).cumprod() * 100

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        # Titlul dinamic care folosește TAG-ul evenimentului trimis din main
        title_suffix = (
            "🚨 PANICĂ DETECTATĂ (Semnificativ Statistic)"
            if is_significant
            else "Nesemnificativ (Absorbție rapidă a șocului / Zgomot)"
        )
        fig.suptitle(
            f"{self.event_name}\nImpact structural asupra: {self.ticker_name} ({self.event_date.date()}) | {title_suffix}",
            fontsize=14,
            fontweight="bold",
        )

        # GRAFICUL 1: Variații procentuale zilnice
        ax1.plot(
            plot_returns.index,
            plot_returns.values,
            label="Randament Real (Zilnic)",
            color="red",
            marker="o",
            markersize=4,
        )
        ax1.axhline(
            y=expected_daily_return,
            color="blue",
            linestyle="--",
            label="Așteptare Normală (Baseline)",
        )

        event_mask = (plot_returns.index >= event_start) & (
            plot_returns.index <= event_end
        )
        event_dates = plot_returns.index[event_mask]

        if len(event_dates) > 0:
            ax1.fill_between(
                event_dates,
                plot_returns.values[event_mask],
                expected_daily_return,
                color="red",
                alpha=0.3,
                label="Abnormal Return (Șocul)",
            )

        ax1.axvline(
            x=self.event_date, color="black", linestyle=":", label="Ziua Știrii (0)"
        )
        ax1.set_ylabel("Randament Zilnic (%)")
        ax1.legend(loc="upper left")
        ax1.grid(True, alpha=0.3)

        # GRAFICUL 2: Valoarea efectivă cumulată (Plecând de la 100)
        ax2.plot(
            real_cumulative.index,
            real_cumulative.values,
            label="Valoarea Portofoliului (Realitate)",
            color="darkred",
            linewidth=2,
        )
        ax2.plot(
            real_cumulative.index,
            expected_cumulative,
            label="Valoare Teoretică (Fără Criză)",
            color="navy",
            linestyle="--",
            linewidth=2,
        )

        if len(event_dates) > 0:
            ax2.fill_between(
                event_dates,
                real_cumulative.values[event_mask],
                expected_cumulative[event_mask],
                color="orange",
                alpha=0.4,
                label="Pierdere cumulată din șoc",
            )

        ax2.axvline(x=self.event_date, color="black", linestyle=":")
        ax2.axvspan(
            event_start,
            event_end,
            color="gray",
            alpha=0.1,
            label="Fereastra analizată [-2, +7] zile",
        )

        ax2.set_ylabel("Valoare Portofoliu (Start = 100)")
        ax2.set_xlabel("Timp")
        ax2.legend(loc="upper left")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        plt.show()
