import matplotlib.pyplot as plt


class Plot:
    def __init__(self, ticker_name, event_date):
        self.ticker_name = ticker_name
        self.event_date = event_date

    def draw_event_study(
        self, event_dates_index, real_returns, normal_returns, is_significant
    ):
        """
        Desenează graficul comparativ și hașurează zona de 'Abnormal Return'.
        """
        plt.figure(figsize=(10, 5))

        # Plotăm ce s-a întâmplat de fapt
        plt.plot(
            event_dates_index,
            real_returns,
            label="Randament Real (Șocul)",
            color="red",
            marker="o",
        )

        # Plotăm ce ar fi fost normal să se întâmple
        plt.plot(
            event_dates_index,
            normal_returns,
            label="Randament Așteptat (Normal)",
            color="blue",
            linestyle="--",
        )

        # MAGIA: Hașura din caietul tău (vertical bars between)
        plt.fill_between(
            event_dates_index,
            real_returns,
            normal_returns,
            color="red",
            alpha=0.3,
            label="Abnormal Return (Panica)",
        )

        # Adăugăm concluzia testului statistic direct pe grafic
        title_suffix = (
            "🚨 SEMNIFICATIV STATISTIC (Panică Reală)"
            if is_significant
            else "Nu prea a afectat mult (Zgomot)"
        )

        plt.title(
            f"Efectul știrii din {self.event_date.date()} asupra {self.ticker_name}\n{title_suffix}"
        )
        plt.xlabel("Zile față de eveniment")
        plt.ylabel("Randament Zilnic")
        plt.axvline(
            x=self.event_date,
            color="black",
            linestyle=":",
            label="Ziua Evenimentului (0)",
        )
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()
