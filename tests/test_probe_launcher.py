import pytest

from probe_launcher import ProbeLauncher

class TestProbeLauncher:

    values = { 
        (7, 2, 3),
        (6, 3, 6),
        (6, 9, 45),
        (9, 0, 0),
        (17, -4, None)
    }

    @pytest.mark.parametrize("dx,dy,result", values)
    def test_launch(self, dx, dy, result):
        pl = ProbeLauncher((20, 30), (-5, -10))
        assert pl.launch(dx, dy) == result

    def test_maximize_height(self):
        pl = ProbeLauncher((20, 30), (-5, -10))
        assert pl.maximize_height() == 45

    def test_count_hits(self):
        pl = ProbeLauncher((20, 30), (-5, -10))
        assert pl.count_hits() == 112
