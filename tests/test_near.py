
from testbook import testbook

@testbook('../near/near_sim_postencounter_doppler.ipynb', execute=True, timeout=600)
def test_near_sim_postencounter_doppler(tb):
	tb.execute()

@testbook('../near/near_sim_postencounter_constlag.ipynb', execute=True, timeout=600)
def test_near_sim_postencounter_doppler(tb):
	tb.execute()

@testbook('../near/near_sim_postencounter_scaledlag.ipynb', execute=True, timeout=600)
def test_near_sim_postencounter_doppler(tb):
	tb.execute()

@testbook('../near/near_gapcheck.ipynb', execute=True)
def test_gapcheck(tb):
    tb.execute()

@testbook('../near/near_sim_ssn_fitlosdoppler_trajectory.ipynb', execute=True)
def test_near_sim_ssn_fitlosdoppler_trajectory(tb):
	tb.execute()

@testbook('../near/near_sim_ssn_fitlosrange_trajectory.ipynb', execute=True)
def test_near_sim_ssn_fitlosrange_trajectory(tb):
	tb.execute()

@testbook('../near/near_sim_ssn_residuals.ipynb', execute=True)
def test_near_sim_ssn_residuals(tb):
	tb.execute()

@testbook('../near/near_sim_ssn_revfit_altair.ipynb', execute=True)
def test_near_sim_ssn_revfit_altair(tb):
	tb.execute()

@testbook('../near/near_sim_ssn_revfit_doppler.ipynb', execute=True)
def test_near_sim_ssn_revfit_doppler(tb):
	tb.execute()

@testbook('../near/near_sim_ssn_revfit_millstone.ipynb', execute=True)
def test_near_sim_ssn_revfit_millstone(tb):
	tb.execute()

@testbook('../near/near_sim_ssn_revfit_range.ipynb', execute=True)
def test_near_sim_ssn_revfit_range(tb):
	tb.execute()

@testbook('../near/near_ssntrack.ipynb', execute=True)
def test_near_ssntrack(tb):
	tb.execute()

