# -*- coding: utf-8 -*-
"""
Created on Fri May 23 18:23:34 2025

@author: BlankAdventure
"""

import numpy as np
from units import handle_units

def calc_capacitive_reactance(c: float, f: float) -> complex:
    '''
    Calculates the capacitive reactance for capacitor c (F) at frequency f (Hz)
    '''
    return 1/(1j*2*np.pi*f*c)

def calc_inductive_reactance(l: float, f: float) -> complex:
    '''
    Calculates the inductive reactance for inductor l (H) at frequency f (Hz)
    '''
    return 1j*2*np.pi*f*l

def combine_parallel(z1: complex, z2: complex) -> complex:
    '''
    Adds two elements (z1, z2) in parallel.
    '''    
    return (z1*z2)/(z1+z2)

def combine_series(z1: complex, z2: complex) -> complex:
    '''
    Adds two elements (z1, z2) in series.
    '''    
    return z1 + z2

def build_tline(num_blocks: int, L: float, r0: float, l0: float, g0: float, c0: float) -> list[tuple[str,float]]:
    '''    

    Parameters
    ----------
    num_blocks : int
        Number of segments to simulate.
    L : float
        Length of transmission line [m].
    r0 : float
        per-unit resistance [ohm/m].
    l0 : float
        per-unit inductance [H/m].
    g0 : float
        per-unit conductance [mohs/m].
    c0 : float
        per-unit capacitance [F/m].

    Returns
    -------
    list[tuple[str,float]]
        List of components properly arranged in transmission line lumped model
        order.
    '''
    r0 = handle_units(r0)
    l0 = handle_units(l0)
    g0 = handle_units(g0)
    c0 = handle_units(c0)
    
    a = L / num_blocks
    single_blk = [('rs',r0*a),('ls',l0*a),('rp',1/(g0*a)),('cp',c0*a)]
    return single_blk*num_blocks


def calc_zin(component_list: list[tuple[str,float]], freq: float, load: complex) -> complex:
    '''    

    Parameters
    ----------
    component_list : list[tuple[str,float]]
        List of tuples of components following the specification:
            ('[r|l|c][s|p]', value)
    freq : float
        Frequency [Hz]
    load : complex
        Terminating load [ohms].

    Returns
    -------
    complex
        Impedance looking into the circuit.

    '''
    z_prev = load
    
    for item in reversed(component_list):    
        
        component = item[0][0].lower()
        orientation = item[0][-1].lower()
        value = handle_units(item[1])
        
        match component:
            case "l":
                z = calc_inductive_reactance(value, freq)
            case "c":
                z = calc_capacitive_reactance(value, freq)
            case "r":
                z = value
            case _:
                raise ValueError(f"{component} is not a valid component. Must be l,c,r.")
                
        match orientation:
            case "s":
                z_new = combine_series(z, z_prev)
            case "p":
                z_new = combine_parallel(z, z_prev)
            case _:
                raise ValueError(f"{orientation} is not a valid orientation. Must be s, p")
        
        z_prev = z_new        
    return z_prev
        

#comps = [('cp','10n'), ('ls','50n')]
#z = calc_zin(comps, 1e6, 25)
#print(z)
#zo = calc_zin([('cp','31.83p'),('ls','55.7n.')],100*1e6,25-10j)
#print(zo)