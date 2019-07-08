import uuid
import textwrap
import collections

import qcelemental as qcel

from ..molecule import Molecule


def muster_and_format_molecule_and_basis_for_gamess(molrec, ropts, qbs, verbose=1):
    kwgs = {'accession': uuid.uuid4(), 'verbose': verbose}
    units = 'Bohr'

    native_puream = qbs.has_puream()
    atom_basisset = qbs.print_detail_gamess(return_list=True)

    gamess_data_record_cart = qcel.molparse.to_string(molrec, dtype='gamess', units=units, atom_format=None, ghost_format=None, width=17, prec=12)
    all_atom_lines = gamess_data_record_cart.splitlines()[3:]

    qmol = Molecule(molrec)
    qmol.update_geometry()

    # PSI: FullPointGroupList = ["ATOM", "C_inf_v", "D_inf_h", "C1", "Cs", "Ci", "Cn", "Cnv", "Cnh", "Sn", "Dn", "Dnd", "Dnh", "Td", "Oh", "Ih"]
    # GMS:                                                      C1    Cs    Ci    Cn    Cnv    Cnh          Dn    Dnd    Dnh    Td    Oh
    # GMS:                        Dnh-2   Cnv-4      Dnh-4                                            S2n
    # GMS:    T, Th, O
    # GAMESS Manual: "For linear molecules, choose either Cnv or Dnh, and enter NAXIS as 4. Enter atoms as Dnh with NAXIS=2."

    pg = qmol.full_point_group_with_n()
    if pg == 'ATOM':
        pgn, naxis = 'Dnh', 2
    elif pg == 'C_inf_v':
        pgn, naxis = 'Cnv', 4 
    elif pg == 'D_inf_h':
        pgn, naxis = 'Dnh', 4
    elif pg == 'Sn':
        pgn, naxis = 'S2n', qmol.full_pg_n() / 2  # n/2n never tested
    else:
        pgn, naxis = pg, qmol.full_pg_n()

    uniq_atombas_lines = gamess_data_record_cart.splitlines()[:2]  # $data and card -1-
    if pg == 'C1':
        uniq_atombas_lines.append(f""" {pgn}""")  # card -2-
        # no empty lines for cards -3- and -4- when C1 symmetry
    elif pg == 'Cs':
        uniq_atombas_lines.append(f""" {pgn}""")  # card -2-
        uniq_atombas_lines.append('')  # empty cards -3- and -4-
    elif pg == 'Ci':
        uniq_atombas_lines.append(f""" {pgn}""")  # card -2-
        uniq_atombas_lines.append('')  # empty cards -3- and -4-
    else:
        uniq_atombas_lines.append(f""" {pgn} {naxis}""")  # card -2-
        uniq_atombas_lines.append('')  # empty cards -3- and -4-

    for iat in range(qmol.natom()):
        if iat == qmol.unique(qmol.atom_to_unique(iat)):
            uniq_atombas_lines.append(all_atom_lines[iat])  # card -5U-
            uniq_atombas_lines.extend(atom_basisset[iat].splitlines()[1:])  # cards -6U- and -7U-
            uniq_atombas_lines.append('')  # card -8U-

    uniq_atombas_lines.append(""" $end""")

    ropts.require('GAMESS', 'contrl__coord', 'unique', **kwgs)
    ropts.require('GAMESS', 'contrl__units', {'Bohr': 'bohr', 'Angstrom': 'angs'}[units], **kwgs)
    ropts.require('GAMESS', 'contrl__icharg', int(molrec['molecular_charge']), **kwgs)
    ropts.require('GAMESS', 'contrl__mult', molrec['molecular_multiplicity'], **kwgs)
    ropts.require('GAMESS', 'contrl__ispher', {True: 1, False: -1}[native_puream], **kwgs)

    return '\n'.join(uniq_atombas_lines)


def muster_and_format_molecule_and_basis_for_gamess_efp(molrec, ropts, qbs, efpnat=0, verbose=1):
    kwgs = {'accession': uuid.uuid4(), 'verbose': verbose}
    units = 'Bohr'

    print('uster_and_format_mol_gamess_efp', efpnat)
    native_puream = qbs.has_puream()
    atom_basisset = qbs.print_detail_gamess(return_list=True)

    gamess_data_record_cart = qcel.molparse.to_string(molrec, dtype='gamess', units=units, atom_format=None, ghost_format=None, width=17, prec=12)
    all_atom_lines = gamess_data_record_cart.splitlines()[3:]

    qmol = Molecule(molrec)
    qmol.update_geometry()

    #gamess_method = input_model.model.dict()['method']
    #if gamess_method == 'gms-makefp':
    #   print('haaaah')

    uniq_atombas_lines = gamess_data_record_cart.splitlines()[:2]  # $data and card -1-
    #print('gamess_data_record_cart =','\n', gamess_data_record_cart)  
    #print('gamess_data_record_cart2 =','\n', gamess_data_record_cart.splitlines()[:2])
    #print('gamess_data_record_cart3 =','\n')
    #print('uniq_atombas_lines =', uniq_atombas_lines)
   
    uniq_atombas_lines.pop()
    uniq_atombas_lines.pop()
    uniq_atombas_lines.append(""" $efrag""")
    uniq_atombas_lines.append(""" """)

#    mysteryvalue=3
    mysteryvalue=efpnat

    for iat in range(0,qmol.natom(),mysteryvalue):
        uniq_atombas_lines.append("""FRAGNAME=FRAGNAME""")
        for fragat in range(iat,iat+mysteryvalue):
            current_line=all_atom_lines[fragat].split()
            uniq_atombas_lines.append("A{0:0>2}{1} {2:>20} {3:>20} {4:>20}".format(fragat%mysteryvalue+1,current_line[0],current_line[2],current_line[3],current_line[4]))

    uniq_atombas_lines.append(""" $end""")

    ropts.require('GAMESS', 'contrl__coord', 'fragonly', **kwgs)
    ropts.require('GAMESS', 'contrl__units', {'Bohr': 'bohr', 'Angstrom': 'angs'}[units], **kwgs)
    ropts.require('GAMESS', 'contrl__icharg', int(molrec['molecular_charge']), **kwgs)
    ropts.require('GAMESS', 'contrl__mult', molrec['molecular_multiplicity'], **kwgs)
    ropts.require('GAMESS', 'contrl__ispher', {True: 1, False: -1}[native_puream], **kwgs)

    return '\n'.join(uniq_atombas_lines)


def format_option_for_gamess(opt, val, lop_off=True):
    """Reformat `val` for option `opt` from python into GAMESS-speak."""

    text = ''

    # Transform booleans into Fortran booleans
    if str(val) == 'True':
        text += '.true.'
    elif str(val) == 'False':
        text += '.false.'

    # No Transform
    else:
        text += str(val).lower()

    if lop_off:
        return opt[7:].lower(), text
    else:
        return opt.lower(), text


def format_options_for_gamess(options):
    """From GAMESS-directed, non-default options dictionary `options`, write a GAMESS deck."""

    grouped_options = collections.defaultdict(dict)
    for group_key, val in options.items():
        group, key = group_key.split('__')
        grouped_options[group][key] = val

    grouped_lines = {}
    for group, opts in sorted(grouped_options.items()):
        line = []
        line.append(f'${group.lower()}')
        for key, val in grouped_options[group].items():
            line.append('='.join(format_option_for_gamess(key, val, lop_off=False)))
        line.append('$end\n')
        grouped_lines[group] = textwrap.fill(' '.join(line), initial_indent=' ', subsequent_indent='  ')

    return '\n'.join(grouped_lines.values()) + '\n'
