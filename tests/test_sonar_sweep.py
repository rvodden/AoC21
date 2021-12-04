import io
from sonar_sweep import sonar_sweep


class TestSonarSweep:

    def test_provided_example(self, monkeypatch):
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
        assert sonar_sweep(depths) == 7
