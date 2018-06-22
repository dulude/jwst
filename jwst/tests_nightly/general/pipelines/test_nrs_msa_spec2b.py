import os
import pytest
import shutil

from astropy.io import fits as pf
from jwst.pipeline.calwebb_spec2 import Spec2Pipeline

pytestmark = [
    pytest.mark.usefixtures('_jail'),
    pytest.mark.skipif(not pytest.config.getoption('bigdata'),
                       reason='requires --bigdata')
]

def test_nrs_msa_spec2b(_bigdata):
    """
    Regression test of calwebb_spec2 pipeline performed on NIRSpec MSA data,
    including barshadow correction.
    """
    file_in = os.path.join(_bigdata, 'pipelines',
                       'jw95065_nrs_msaspec_barshadow.fits')

    step = Spec2Pipeline()
    step.output_file='jw95065_nrs_msaspec_barshadow_cal.fits'
    step.save_bsub = False
    step.save_results = True
    step.resample_spec.skip = True
    step.resample_spec.save_results = True
    step.cube_build.save_results = True
    step.extract_1d.save_results = True
    step.run(file_in)

    ignore_keywords = ['DATE','CAL_VER','CAL_VCS','CRDS_VER','CRDS_CTX']

    # compare _cal file
    na = 'jw95065_nrs_msaspec_barshadow_cal.fits'
    nb = os.path.join(_bigdata,'pipelines',
                      'jw95065_nrs_msaspec_barshadow_cal_ref.fits')
    h = pf.open(na)
    href = pf.open(nb)
    result = pf.diff.FITSDiff(h,
                              href,
                              ignore_hdus=['ASDF'],
                              ignore_keywords=ignore_keywords,
                              rtol = 0.00001)
    assert result.identical, result.report()

    na = 'f170lp-g235m_mos_observation-6-c0e0_001_dn_nrs1_mod_s2d.fits'
    nb = _bigdata+'/pipelines/F170LP-G235M_MOS_observation-6-c0e0_001_DN_NRS1_s2d_ref.fits'
    h = pf.open(na)
    href = pf.open(nb)
    result = pf.diff.FITSDiff(h,
                              href,
                              ignore_hdus=['ASDF'],
                              ignore_keywords=ignore_keywords,
                              rtol = 0.00001)
    assert result.identical, result.report()

    # compare _x1d file
    na = 'jw95065_nrs_msaspec_barshadow_x1d.fits'
    nb = os.path.join(_bigdata,'pipelines',
                      'jw95065_nrs_msaspec_barshadow_x1d_ref.fits')
    h = pf.open(na)
    href = pf.open(nb)
    result = pf.diff.FITSDiff(h,
                              href,
                              ignore_hdus=['ASDF'],
                              ignore_keywords=ignore_keywords,
                              rtol = 0.00001)
    assert result.identical, result.report()
