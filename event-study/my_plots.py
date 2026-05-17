import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Plot:
    def __init__(self, ticker_name, event_date):
        self.ticker_name = ticker_name
        self.event_date = pd.to_datetime(event_date)

    def draw_event_study(
        self, plot_data, event_start, event_end, expected_daily_return, is_significant
    ):
        """
        Desenează 2 grafice: Randamente (sus) și Valoare Cumulată Baza 100 (jos).
        """
        # Calculăm randamentele pentru toată perioada lărgită de zoom
        plot_returns = plot_data.pct_change().dropna()

        # MAGIA: Evoluția valorii (Cumulăm randamentele plecând de la o bază de 100 RON/USD)
        real_cumulative = (1 + plot_returns).cumprod() * 100

        # Creăm linia așteptată (cum s-ar fi cumulat banii dacă aveam doar zile normale)
        expected_returns_array = np.repeat(expected_daily_return, len(plot_returns))
        expected_cumulative = (1 + expected_returns_array).cumprod() * 100

        # Setăm fereastra mare cu 2 grafice care împart aceeași axă de timp (X)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        title_suffix = (
            "🚨 SEMNIFICATIV STATISTIC (Panică Reală)"
            if is_significant
            else "Nesemnificativ statistic (Zgomot/Recuperare rapidă)"
        )
        fig.suptitle(
            f"Analiza șocului din {self.event_date.date()} asupra {self.ticker_name}\n{title_suffix}",
            fontsize=14,
            fontweight="bold",
        )

        # ---------------------------------------------------------
        # GRAFICUL 1: RANDAMENTE ZILNICE (Cel pe care îl aveai deja)
        # ---------------------------------------------------------
        ax1.plot(
            plot_returns.index,
            plot_returns.values,
            label="Randament Real",
            color="red",
            marker="o",
            markersize=4,
        )
        ax1.axhline(
            y=expected_daily_return,
            color="blue",
            linestyle="--",
            label="Randament Normal Așteptat",
        )

        # Masking - Căutăm doar datele care pică exact în fereastra de eveniment ca să le hașurăm
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
                label="Abnormal Return (Șocul calculat)",
            )

        ax1.axvline(
            x=self.event_date, color="black", linestyle=":", label="Ziua Știrii (0)"
        )
        ax1.set_ylabel("Randament Zilnic (%)")
        ax1.legend(loc="upper left")
        ax1.grid(True, alpha=0.3)

        # ---------------------------------------------------------
        # GRAFICUL 2: VALOAREA EFECTIVĂ (Cumulată)
        # ---------------------------------------------------------
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
            label="Valoare Așteptată (Fără criză)",
            color="navy",
            linestyle="--",
            linewidth=2,
        )

        # Hașurăm cu portocaliu gap-ul (prăbușirea banilor) doar în fereastra analizată
        if len(event_dates) > 0:
            ax2.fill_between(
                event_dates,
                real_cumulative.values[event_mask],
                expected_cumulative[event_mask],
                color="orange",
                alpha=0.4,
                label="Pierdere din șoc",
            )

        ax2.axvline(x=self.event_date, color="black", linestyle=":")

        # Adăugăm un fundal gri discret care marchează TOATĂ zona de analiză [-2, +7]
        ax2.axvspan(
            event_start,
            event_end,
            color="gray",
            alpha=0.1,
            label="Fereastra de Analiză a Evenimentului",
        )

        ax2.set_ylabel("Valoare Normalizată (Start = 100)")
        ax2.set_xlabel("Timp")
        ax2.legend(loc="upper left")
        ax2.grid(True, alpha=0.3)

        # Ajustăm aspectul final ca să nu se încalece titlurile
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        plt.show()
