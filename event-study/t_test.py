import numpy as np
from scipy import stats


def t_test_if_significant(abnormal_returns, historical_std):
    """
    abnormal_returns: diferența dintre randamentul real și cel prezis.
    historical_std: volatilitatea (abaterea standard) normală a acțiunii.
    """
    # Calculăm media randamentelor anormale în fereastra de eveniment
    mean_ar = np.mean(abnormal_returns)
    n = len(abnormal_returns)

    # Formula clasică de t-statistic pentru Event Study
    t_stat = mean_ar / (historical_std / np.sqrt(n))

    # Calculăm p-value (test bilateral)
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n - 1))

    threshold = 0.05  # Pragul academic standard de 5%

    is_significant = p_value < threshold

    return is_significant, p_value, t_stat
