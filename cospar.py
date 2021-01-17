import sys, os
everestPath = os.path.abspath('everest')
if not everestPath in sys.path:
    sys.path.insert(0, everestPath)

import math
import numpy as np

from everest.h5anchor import Reader, Fetch
F = lambda key: Fetch(f"*/{key}")
reader = Reader('obsvisc', os.path.dirname(__file__))

from everest.window import Canvas
from everest.window.data import Data

with reader.open():
    groupkeys = tuple(reader.h5file.keys())
paramkeys = (
    'tauRef',
    'f',
    'aspect',
    'etaDelta',
    'etaRef',
    'alpha',
    'H',
    'flux',
    'kappa',
    )
datakeys = (
    't',
    'dt',
    'Nu',
    'Nu_freq',
    'Nu_min',
    'Nu_range',
    'VRMS',
    'strainRate_outer_av',
    'strainRate_outer_min',
    'strainRate_outer_range',
    'stressAng_outer_av',
    'stressAng_outer_min',
    'stressAng_outer_range',
    'stressRad_outer_av',
    'stressRad_outer_min',
    'stressRad_outer_range',
    'temp_av',
    'temp_min',
    'temp_range',
    'velAng_outer_av',
    'velAng_outer_min',
    'velAng_outer_range',
    'velMag_range',
    'visc_av',
    'visc_min',
    'visc_range',
    'yieldFrac'
    )

def highlight_case(f, aspect, tauRef, freq = 1):

    tF = dict(zip((1, 2), ('_built_peaskauslu-thoesfthuec', '_built_oiskeaosle-woatihoo')))[freq]

    cut = reader[
        (F('f') == f) \
        & (F('aspect') == aspect) \
        & (F('temperatureField') == '_built_peaskauslu-thoesfthuec') \
        ]
    datas = sorted(reader[cut : ('tauRef', 't', 'Nu')].values())
    t, Nu = dict((tau, ds) for tau, *ds in datas)[tauRef]

    canvas = Canvas(size = (12, 6))
    ax = canvas.make_ax()
    ax.line(
        Data(t, label = "Dimensionless time"),
        Data(Nu, label = "Nusselt number"),
        )
    ax.axes.title = f"MS98 Nusselt profile\nf = {f}, aspect = {aspect}, tauRef = 10^{math.log10(tauRef)}"
    ax.grid.colour = 'grey'

    return canvas