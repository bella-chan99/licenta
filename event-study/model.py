import pandas as pd
import numpy as np


class Model:
    def __init__(self, historical_data):
        """
        historical_data: un pandas Series cu prețurile din fereastra de estimare (ex: 100 de zile înainte).
        """
        # Calculăm randamentele zilnice procentuale din trecut
        self.historical_returns = historical_data.pct_change().dropna()

        # 'Normalul' este media randamentelor din acea perioadă calmă
        self.expected_daily_return = self.historical_returns.mean()

        # Salvăm și volatilitatea (abaterea standard) pentru t-test
        self.historical_std = self.historical_returns.std()

    def predict(self, event_window_length):
        """
        Prezice randamentul 'normal' pentru zilele din fereastra de eveniment.
        Returnează un array cu valoarea așteptată repetată de 'n' ori.
        """
        return np.repeat(self.expected_daily_return, event_window_length)
