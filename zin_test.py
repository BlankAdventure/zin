# -*- coding: utf-8 -*-
"""
Created on Fri May 23 18:56:06 2025

@author: BlankAdventure
"""


import unittest

from zin import (
    calc_capacitive_reactance,
    calc_inductive_reactance,
    combine_parallel,
    combine_series,
    calc_zin,
    build_tline
)

import units as units

class Tests_units(unittest.TestCase):
    def test_valid(self):
        inputs = ['30n','.1m','0.25k']
        expected = [3e-8, 0.0001, 250]        
        for (a,b) in zip(inputs, expected):
            result = units.decode_unit(a)
            self.assertAlmostEqual(result,b,places=8)

    def test_invalid(self):        
        invalid_inputs = ['3b','0.1','M','0.34km', '-0.15M']
        for test in invalid_inputs:
            self.assertRaises(ValueError, units.decode_unit, test )
            
    def test_handle(self):
        result = units.handle_units('15.5m') #valid input
        self.assertEqual(result,0.0155)

        result = units.handle_units(10e-3) #valid input
        self.assertEqual(result,10e-3)

        self.assertRaises(TypeError, units.handle_units, [])


class Tests_zin(unittest.TestCase):    
    def test_c_react(self):        
        react = calc_capacitive_reactance(1e-8, 1e6)
        self.assertAlmostEqual(react, -1j*15.91549, delta=0.01)
        
    def test_l_react(self):        
        react = calc_inductive_reactance(1e-4, 1e5)
        self.assertAlmostEqual(react,1j*62.83185, delta=0.01)
        
    def test_combine_series(self):
        z1 = 3 + 1j*4
        z2 = 10 - 1j*15        
        combined = combine_series(z1, z2)        
        self.assertEqual(combined,13-1j*11)
        
    def test_combine_parallel(self):
        z1 = 3 + 1j*4
        z2 = 10 - 1j*15        
        combined = combine_parallel(z1, z2)        
        self.assertAlmostEqual(combined,4.22413+3.18965j,delta=0.01)
        
    def test_zin_simple_series_r(self):
        components = [('rs',20)]        
        zin = calc_zin(components, 10e6, 25)
        self.assertEqual(zin, 45)
        
    def test_match_lc(self):
        zo = calc_zin([('cp',31.83*1e-12),('ls',55.70*1e-9)],100*1e6,25-10j)
        self.assertAlmostEqual(zo,50+0j, delta=0.01)   
        
        zo = calc_zin([('lp',79.58*1e-9),('cs',106.1*1e-12)],100*1e6,25-10j)
        self.assertAlmostEqual(zo,50+0j, delta=0.01)   
        
    def test_match_pi(self):
        zo = calc_zin([('cp',95.5*1e-12),('ls',41.34*1e-9), ('cp',142.2*1e-12)],100*1e6,25+10j)
        self.assertAlmostEqual(zo,50+0j, delta=0.5)   
        
    def test_match_t(self):
        zo = calc_zin([('ls',95.5*1e-9),('cp',36.03*1e-12), ('ls',161.78*1e-9)],100*1e6,60-10j)
        self.assertAlmostEqual(zo,20+0j, delta=0.5)   
        
    def test_build_tline(self):
        R = 1e-3; 
        G = 1e-5;
        L = 25*1e-8; 
        C = 1*1e-10;
        freq = 10e5
        l = 24 
        n = 1000
        tline = build_tline(n, l, R, L, G, C)
        zo = calc_zin(tline,freq,25)
        self.assertAlmostEqual(zo,38.31+28.68j, delta=0.01)
        
    def test_build_tline_quarter(self):
        R = 1e-8 
        G = 1e-8 
        L = 25*1e-8; 
        C = 1*1e-10;
        l = 20*(3/4)
        freq = 10e6
        n = 1000
        tline = build_tline(n, l, R, L, G, C)
        zo = calc_zin(tline,freq,12.5)
        self.assertAlmostEqual(zo,(50*50/12.5), delta=3)
        