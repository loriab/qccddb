#! single-point UHF/cc-pVDZ  on NH2 
import os
import sys
from addons import *
from utils import *
import qcdb

nh2= qcdb.set_molecule('''
           N        0.08546       -0.00020       -0.05091
           H       -0.25454       -0.62639        0.67895
           H       -0.25454       -0.31918       -0.95813
           ''')
print(nh2)
def check_uhf_hf(return_value, is_df=True):
    if is_df:
        ref     =       -55.566057523877
        nre     =         7.580905897627
    else:
        ref     =       -55.566057523877
        nre     =         7.580905897627

    assert compare_values(ref, qcdb.get_variable('HF TOTAL ENERGY'), 2, 'scf')
    assert compare_values(nre, qcdb.get_variable('NUCLEAR REPULSION ENERGY', 5, 'nre')

@using_nwchem
def test_1_hf():
    qcdb.set_options({
        'basis'     : 'cc-pvdz',
        'memory'    : '400 mb',
        'nwchem_scf': 'uhf',
        'nwchem_scf_nopen': 1,
        'nwchem_scf_thresh': 1.0e-8
        })
    print('Testing hf...')
    val = qcdb.energy('nwc-hf')
    check_uhf_hf(val, is_df=True)
