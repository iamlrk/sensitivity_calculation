import matplotlib.pyplot as plt
from math import exp 
import math 

energy = [15,20,30,40,50,60,70,80,90,100,150,300,400,500]
sigma = 3
A = 825
T = 1e5 
omega = 1 ##solid angle of aperture in staradians 
# delta_E = 10 ##bandwidth over which the measurement is made in keV 


mu = [9.148E+01, 4.222E+01, 1.385E+01, 6.206E+00, 3.335E+00, 2.023E+00,1.48655, 9.501E-01, 0.75255,5.55E-01, 2.491E-01, 1.131E-01,9.327E-02, 8.212E-02] ##mass attentuation coefficient from XCOM based on material used as a function of energy
lambd = 1 ##density * thickness of detector 
epsilon = [] ##efficiency
Bcdb = [] ##cosmic background contribution
B_ph = [] ## shield leakage 
B_ph5 = [0.91,0.91,0.91,0.91,0.91,0.91,0.91,0.91,0.875,0.875,0.825,0.34,0.24,0.24]
x = 5 ##thickness of shield 
Fig_5 = [1.82,1.82,1.82,1.82,1.82,1.82,1.82,1.82,1.75,1.75,1.65,0.68,0.48,0.48] 
Bns = [] ##neutron and spallation background contribution
F_R_c = 4.7 ##read off figure 6 
for i in range(0, len(energy)):
    """detection efficiency"""
    ## ε(E_γ) = (1- exp(-μ_m*λ))
    ep = (1- exp(-mu[i]*lambd))
    epsilon.append(ep)
    """Background noise"""
    ##Cosmic diffuse via the Aperture
    ##dN(E_γ)/dE_γ = 87.4*E_γ^-2.3
    ##B_cdb = Ω*ε(E_γ)* dN(E_γ)/dE_γ
    dN = 87.4*pow(energy[i],-2.3)
    B = omega * epsilon[i]*dN
    Bcdb.append(B)
    ##Shield leakage
    ##B_ph(dE_γ) = B_Ph5cm * E_γ *exp(1-x/5)
    ph = B_ph5[i]* exp(1-(x/5))
    B_ph.append(ph)
    ##Spallation induced background   
    ns = F_R_c * Fig_5[i]
    Bns.append(ns)


B_t = []
for i in range (0, len(energy)):
    total = Bcdb[i] + B_ph[i] + Bns[i]
    B_t.append(total)

"""Continuum sensitivity"""
F_min = [] 
for j in range(0, len(energy)):
    F = (sigma/epsilon[j])*math.sqrt((4*B_t[j])/(A*T*energy[j]))   
    F_min.append(F)

plt.plot(energy, F_min)
plt.xlabel('energy/keV')
plt.ylabel('photons/cm^2/s/keV')
plt.title('Continuum Sensitivity Curve')
plt.show()