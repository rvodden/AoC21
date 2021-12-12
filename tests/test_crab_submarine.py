import pandas as pd

from crab_submarine import CrabSubmarine

class TestCrabSubmarine:
    def test_calculate_crab_fuel(self):
        df = pd.DataFrame([16,1,2,0,4,2,7,1,2,14], columns=['positions'])
        assert CrabSubmarine.calculate_crab_fuel(df) == 37