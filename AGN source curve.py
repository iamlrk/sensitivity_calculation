# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 11:31:56 2023

@author: annac
"""

import matplotlib.pyplot as plt
from scipy.integrate import quad
def integrand(x, a, b):
    return a*(pow(x, -b))

energy = []
photons = []
error = []
count = 0
l = 10
h = 20
a = 2.092206715e-3
b = 1.56

for i in range(0, 50):
    I = quad(integrand, l, h, args=(a,b))
    energy.append(l)
    photons.append(I[0]) ##photons/cm2/s/keV
    error.append(I[1]) ##error on integral calculation
    l = l + 10
    h = h + 10
    count = count + 1
 

plt.step(energy, photons)
plt.ylabel('Photons/cm2/s/keV')
plt.xlabel('Energy(keV)')
plt.title('Approximate Emission Spectrum of Circinus Galaxy')
plt.show()
