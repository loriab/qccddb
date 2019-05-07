#! single-point HF/cc-pVDZ (Cartesian) on NH2
import os
import sys
from ..utils import *
from ..addons import *
import qcdb

#nh2 = qcdb.set_molecule('''
 #       N    0.00000000     0.00000000    -0.13636256
  #      H   -0.79970017     0.00000000     0.47726896
   #     H    0.79970017     0.00000000     0.47726896
    #    ''')

nh2= qcdb.set_molecule('''
        N
        H 1 1.008
        H 1 1.008 2 105.0''')
print(nh2)


def check_hf(return_value):
    ref = -55.562683879400
    nre = 7.680543797856

    assert compare_values(ref, qcdb.get_variable('HF TOTAL ENERGY'), 5, 'hf total')
    assert compare_values(nre, qcdb.get_variable('NUCLEAR REPULSION ENERGY'), 5, 'nre')


@using_nwchem
def test_1_rohf():
    qcdb.set_options({
        'basis': 'cc-pVDZ',
        'memory': '2500 mb',
        'nwchem_scf__rohf': True,
        'nwchem_scf__rhf' : False,
        'nwchem_scf__nopen': 1,
        'scf__e_convergence': 1.0e-8,
        'nwchem_scf__thresh': 1.0e-8,
    })
    print('Testing HF energy ...')
    val = qcdb.energy('nwc-hf')
    check_hf(val)
