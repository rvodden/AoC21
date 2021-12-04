import io

import pandas as pd

from sonar_sweep import SonarSweep


class TestSonarSweep:

    def test_count_increases(self, monkeypatch):
        depths = [199,
                  200,
                  208,
                  210,
                  200,
                  207,
                  240,
                  269,
                  260,
                  263]
        assert SonarSweep.count_increases(pd.DataFrame(depths)) == 7
