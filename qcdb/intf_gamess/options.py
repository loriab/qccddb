from ..moptions.read_options2 import RottenOption
from ..moptions import parsers


def load_gamess_defaults(options):

    # $SYSTEM

    options.add('gamess', RottenOption(
            keyword='system__mwords',
            default=400,
            validator=parsers.positive_integer,
            glossary="""Maximum replicated memory which your job can use, on every core. Units of 1000^2 words (not 1024^2)."""))


    # $CONTRL

    options.add('gamess', RottenOption(
            keyword='contrl__scftyp',
            default='rhf',
            validator=parsers.enum("RHF UHF ROHF GVB MCSCF NONE"),
            glossary=""""""))

    options.add('gamess', RottenOption(
            keyword='contrl__dfttyp',
            default='none',
            validator=parsers.enum("NONE B3LYP PBE0"),
            glossary=""""""))

    options.add('gamess', RottenOption(
            keyword='contrl__mplevl',
            default=2,
            validator=parsers.intenum("0 2"),
            glossary=""""""))

    options.add('gamess', RottenOption(
            keyword='contrl__cctyp',
            default='none',
            validator=parsers.enum("NONE LCCD CCD CCSD(T) R-CC CR-CC CR-CCL CCSD(TQ) CR-CC(Q) EOM-CCSD CR-EOM CR-EOML IP-EOM2 IP-EOM3A EA-EOM2 EA-EOM3A"),
            glossary=""""""))

    options.add('gamess', RottenOption(
            keyword='contrl__runtyp',
            default='energy',
            validator=parsers.enum("ENERGY GRADIENT HESSIAN MAKEFP"),
            glossary="""For makefp runs, generally use 6-311++G(3d2pf) basis set"""))

    options.add('gamess', RottenOption(
            keyword='contrl__cityp',
            default='none',
            validator=parsers.enum("NONE CIS SFCIS ALDET ORMAS FSOCI GENCI GUGA"),
            glossary=""""""))

    options.add('gamess', RottenOption(
            keyword='contrl__maxit',
            default=30,
            validator=parsers.positive_integer,  # psi4 maxiter
            glossary=""""""))

    options.add('gamess', RottenOption(
            keyword='contrl__icharg',
            default=0,
            validator=parsers.integer,
            glossary=""""""))

    options.add('gamess', RottenOption(
            keyword='contrl__mult',
            default=1,
            validator=parsers.positive_integer,
            glossary=""""""))

    options.add('gamess', RottenOption(
            keyword='contrl__coord',
            default='unique',
            validator=parsers.enum("UNIQUE HINT PRINAXIS ZMT ZMTMPC FRAGONLY CART"),
            glossary=""""""))

    options.add('gamess', RottenOption(
            keyword='contrl__units',
            default='angs',
            validator=parsers.enum("ANGS BOHR"),
            glossary="""Distance units, any angles must be in degrees."""))

    options.add('gamess', RottenOption(
            keyword='contrl__ispher',
            default=-1,
            validator=parsers.intenum("-1 0 1"),
            glossary="""Spherical Harmonics option."""))


    options.add('gamess', RottenOption(
            keyword='basis__gbasis',
            default='sto',
            validator=parsers.enum("STO N21 N31 N311 G3L G3LX"),
            glossary=""""""))


    # $SCF

    options.add('gamess', RottenOption(
            keyword='scf__conv',
            default=1.e-6,
            validator=parsers.parse_convergence,  # psi4 d_convergence
            glossary="""SCF density convergence criteria"""))

    options.add('gamess', RottenOption(
            keyword='scf__ethrsh',
            default=0.5,
            validator=lambda x: float(x),
            glossary="""Energy error threshol for initiating DIIS."""))

    options.add('gamess', RottenOption(
            keyword='scf__dirscf',
            default=False,
            validator=parsers.boolean,
            glossary="""Do activate a direct SCF calculation?"""))


    # $MP2

    options.add('gamess', RottenOption(
            keyword='mp2__nacore',
            default=0,
            validator=parsers.nonnegative_integer,
            glossary="""Omits the first n occupied orbitals from the calculation. Default is chemical core."""))

    options.add('gamess', RottenOption(
            keyword='mp2__nbcore',
            default=0,
            validator=parsers.nonnegative_integer,
            glossary="""same as |gamess__mp2__nacore| for beta orbitals of UHF. Generally equals nacore."""))


    # $CCINP

    options.add('gamess', RottenOption(
            keyword='ccinp__ncore',
            default=0,
            validator=parsers.nonnegative_integer,
            glossary="""Omits the first n occupied orbitals from the calculation. Default is chemical core."""))

    options.add('gamess', RottenOption(
            keyword='ccinp__iconv',
            default=7,
            validator=parsers.positive_integer,
            glossary="""Convergence criterion for the cluster amplitudes."""))


    # $DFT

    options.add('gamess', RottenOption(
            keyword='dft__nrad',  # psi4 dft_angular_points
            default=96,
            validator=parsers.positive_integer,
            glossary="""Number of radial points in the Euler-MacLaurin quadrature."""))

    options.add('gamess', RottenOption(
            keyword='dft__nleb',  # psi4 dft_spherical_points
            default=302,
            validator=parsers.intenum("86 110 146 170 194 302 350 434 590 770 974 1202 1454 1730 2030"),
            glossary="""Number of angular points in the Lebedev grids."""))

    #options.add_int("GAMESS_EOMINP_NSTATE", 1);


    # $CIDET

    options.add('gamess', RottenOption(
            keyword='cidet__ncore',
            default=0,
            validator=parsers.nonnegative_integer,
            glossary="""Total number of orbitals doubly occupied in all determinants."""))

    options.add('gamess', RottenOption(
            keyword='cidet__nact',
            default=1, #None,
            validator=parsers.positive_integer,
            glossary="""Total number of active orbitals."""))

    options.add('gamess', RottenOption(
            keyword='cidet__nels',
            default=2, #None,
            validator=parsers.positive_integer,
            glossary="""Total number of active electrons."""))


    # $MAKEFP

    options.add('gamess', RottenOption(
            keyword='makefp__frag',
            default='FRAGNAME',
            validator=lambda x: x.upper()[:8],
            glossary="""a string of up to 8 letters to identify this EFP.
            For example, WATER or BENZENE or CH3OH or ...
            (default=FRAGNAME, which you can hand edit later)"""))

    options.add('gamess', RottenOption(
            keyword='makefp__screen',
            default=True,
            validator=parsers.boolean,
            glossary="""A flag to generate screening information for the multipole electrostatics,
            and maybe polarizability screening. 
            (default=.TRUE. for RHF, so far ROHF is not coded)"""))

    options.add('gamess', RottenOption(
            keyword='makefp__pol',
            default=True,
            validator=parsers.boolean,
            glossary="""A a flag to generate dipole polarizabilities. (default=.TRUE.)"""))

    options.add('gamess', RottenOption(
            keyword='makefp__exrep',
            default=True,
            validator=parsers.boolean,
            glossary="""A a flag to generate exchange repulsion parameters. (default=.TRUE.)"""))

    options.add('gamess', RottenOption(
            keyword='makefp__chtr',
            default=True,
            validator=parsers.boolean,
            glossary="""A a flag to generate charge transfer parameters.
            (default=.TRUE. for RHF, so far ROHF is not coded)"""))

    options.add('gamess', RottenOption(
            keyword='makefp__ctvvo',
            default=True,
            validator=parsers.boolean,
            glossary="""A a flag to specify what type of charge transfer data is generated. (default=.TRUE.)  
            .FALSE. means all canonical virtuals are used.
            .TRUE. means Valence Virtual Orbitals will be created, by forcing VVOS in $SCF is forced on.
            The VVOs are many fewer in number, so the charge transfer calculation is greatly accelerated."""))

    options.add('gamess', RottenOption(
            keyword='makefp__disp',
            default=True,
            validator=parsers.boolean,
            glossary="""A a flag to generate information for dispersion.
            (default=.TRUE. for RHF, so far ROHF is not coded)"""))
