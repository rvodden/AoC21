import io

import pandas as pd

from sonar_sweep import SonarSweep


class TestSonarSweep:
    def depths(self):
        return pd.DataFrame(
        [199,
                  200,
                  208,
                  210,
                  200,
                  207,
                  240,
                  269,
                  260,
                  263])

    def test_count_increases(self):
        assert SonarSweep.count_increases(pd.DataFrame(self.depths())) == 7

    def test_rolling_windows(self):
        assert SonarSweep.count_increases(SonarSweep.rolling_windows(self.depths())) == 5
