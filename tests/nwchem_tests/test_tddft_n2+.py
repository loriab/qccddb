#Test CIS, TDHF, TDDFT functionality using HF function for spin unrestricted reference with symmetry on
#Need to check out tddft excited states compared to harvester
import os
import sys
from ..addons import *
from ..utils import *
import qcdb

n2_plus = qcdb.set_molecule('''
        N 0.0 0.0 -0.54885
        N 0.0 0.0  0.54885
        ''')
print(n2_plus)

def check_tddft(return_value):
    if is_df:
        ref = -108.945393441525 #ground state
        nre = 23.621832195486
        root1_ex = 0.039837937 #a.u.
        root2_ex = 0.039837937
        root3_ex = 0.116062978
        root4_ex = 0.254048147
        root5_ex = 0.288942035
        root6_ex = 0.288942041
        root7_ex = 0.340791279
        root8_ex = 0.351283436
        root9_ex = 0.363212907
        root10_ex = 0.363212907
        root1_energy = 1.0840 #eV
        root2_energy = 1.0840
        root3_energy = 3.1582
        root4_energy = 6.9130
        root5_energy = 7.8625
        root6_energy = 7.8625
        root7_energy = 9.2734
        root8_energy = 9.5589
        root9_energy = 9.8835
        root10_energy= 9.8835
        #excitation = 0.039837937441
        #excited_energy = -108.905555504084

    assert compare_values(ref, qcdb.get_variable('DFT TOTAL ENERGY'), 5, 'ref')
    assert compare_valeus(nre, qcdb.get_variable('NUCLEAR REPULSION ENERGY'), 5, 'nre')
    assert compare_values(root1_ex, qcdb.get_variable('TDDFT ROOT 1 EXCITATION ENERGY - B2U SYMMETRY'), 5, 'tddft root 1 excitation')
    assert compare_values(root2_ex, qcdb.get_variable('TDDFT ROOT 2 EXCITATION ENERGY - B3U SYMMETRY'), 5, 'tddft root 2 excitation')
    assert compare_values(root3_ex, qcdb.get_variable('TDDFT ROOT 3 EXCITATION ENERGY - B1U SYMMETRY'), 5, 'tddft root 3 excitation')
    assert compare_values(root4_ex, qcdb.get_variable('TDDFT ROOT 4 EXCITATION ENERGY - B1U SYMMETRY'), 5, 'tddft root 4 excitation')
    assert compare_values(root5_ex, qcdb.get_variable('TDDFT ROOT 5 EXCITATION ENERGY - B1U SYMMETRY'), 5, 'tddft root 5 excitation')
    assert compare_values(root6_ex, qcdb.get_variable('TDDFT ROOT 6 EXCITATION ENERGY - AU SYMMETRY'), 5, 'tddft root 6 excitation')
    assert compare_values(root7_ex, qcdb.get_variable('TDDFT ROOT 7 EXCITATION ENERGY - AU SYMMETRY'), 5, 'tddft root 7 excitation')
    assert compare_values(root8_ex, qcdb.get_variable('TDDFT ROOT 8 EXCITATION ENERGY - AU SYMMETRY'), 5, 'tddft root 8 excitation')
    assert compare_values(root9_ex, qcdb.get_variable('TDDFT ROOT 9 EXCITATION ENERGY - AU SYMMETRY'), 5, 'tddft root 9 excitation')
    assert compare_values(root10_ex, qcdb.get_variable('TDDFT ROOT 10 EXCITATION ENERGY - B1U SYMMETRY'), 5, 'tdddft root 10 excitation')
    assert compare_values(root1_energy, qcdb.get_variable('TDDFT ROOT 1 EXCITED STATE ENERGY - B2U SYMMETRY'), 5, 'tddftroot 1 excited state')
    assert compare_values(root2_energy, qcdb.get_variable('TDDFT ROOT 2 EXCITED STATE ENERGY - B3U SYMMETRY'), 5, 'tddft root 2 excited state')
    assert compare_values(root3_energy, qcdb.get_variable('TDDFT ROOT 3 EXCITED STATE ENERGY - B1U SYMMETRY'), 5, 'tddft root 3 excited state')
    assert compare_values(root4_energy, qcdb.get_variable('TDDFT ROOT 4 EXCITED STATE ENERGY - B1U SYMMETRY'), 5, 'tddft root 4 excited state')
    assert compare_values(root5_energy, qcdb.get_variable('TDDFT ROOT 5 EXCITED STATE ENERGY - B1U SYMMETRY'), 5, 'tddft root 5 excited state')
    assert compare_values(root6_energy, qcdb.get_variable('TDDFT ROOT 6 EXCITED STATE ENERGY - AU SYMMETRY'), 5, 'tddft root 6 excited state')
    assert compare_values(root7_energy, qcdb.get_variable('TDDFT ROOT 7 EXCITED STATE ENERGY - AU SYMMETRY'), 5, 'tddft root 7 excited state')
    assert compare_values(root8_energy, qcdb.get_variable('TDDFT ROOT 8 EXCITED STATE ENERGY - AU SYMMETRY'), 5, 'tddft root 8 excited state')
    assert compare_values(root9_energy, qcdb.get_variable('TDDFT ROOT 9 EXCITED STATE ENERGY - AU SYMMETRY'), 5, 'tddft root 9 excited state')
    assert compare_values(root10_energy, qcdb.get_variable('TDDFT ROOT 10 EXCITED STATE ENERGY - B1U SYMMETRY'), 5, 'tddft root 10 excited state')

@using_nwchem
def test_1_dft():
    qcdb.set_options({
        'basis': '6-31g**',
        'memory' : '3000 mb',
        'nwchem_charge': 1,
        'nwchem_dft__xc': 'b3lyp',
        'nwchem_dft__mult': 2,
        'nwchem_tddft__nroots': 10
    })
    print('Testing hf...')
    val = qcdb.energy('nwc-tddft')
    check_tddft(val)
