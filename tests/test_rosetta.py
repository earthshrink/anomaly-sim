
from testbook import testbook

@testbook('../rosetta/rosetta_sim_approach_rangerate.ipynb', execute=True)
def test_rosetta_sim_approach_rangerate(tb):
	tb.execute()

@testbook('../rosetta/rosetta_sim_postencounter_rangerate.ipynb', execute=True, timeout=300)
def test_rosetta_sim_postencounter_rangerate(tb):
	tb.execute()

