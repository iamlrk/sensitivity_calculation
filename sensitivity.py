# based on code written by Anna

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calculate_efficiency(density, thickness, mass_attentuation_coefficients):
    return [1 - np.exp(_mu)*(density * thickness) for _mu in mass_attentuation_coefficients]

def calculate_cosmic_bg(energies, solid_angle, efficiencies):
    return [solid_angle*efficiency*(87.4*energy**(-2.3)) for efficiency, energy in zip(efficiencies, energies)]

def calculate_shield_bg(shield_leakage_bg_count_rates, thickness):
    return [leaks * np.exp(1-(thickness/5)) for leaks in shield_leakage_bg_count_rates]

def calculate_neutron_spallation_bg(rigidity_cut_off, energy_counts): # from fig 5
    return  [rigidity_cut_off * counts for counts in energy_counts]

class Background():
    def __init__(self, 
                 density, 
                 shield_thickness, 
                 mass_attentuation_coefficients, 
                 energies, 
                 solid_angle, 
                 shield_leakage_bg_count_rates,
                 rigidity_cut_off,
                 energy_counts,
                 thickness,
                 area) -> None:
        self.density = density
        self.thickness = thickness 
        self.shield_thickness = shield_thickness 
        self.mass_attentuation_coefficients = mass_attentuation_coefficients 
        self.energies = energies 
        self.solid_angle = solid_angle
        self.shield_leakage_bg_count_rates = shield_leakage_bg_count_rates
        self.rigidity_cut_off = rigidity_cut_off
        self.energy_counts = energy_counts
        self.area = area

    def calculate_efficiency(self):
        self.efficiencies = [1 - np.exp(-_mu*self.density * self.thickness) for _mu in self.mass_attentuation_coefficients]
        return self.efficiencies

    def calculate_cosmic_bg(self):
        self.calculate_efficiency()
        self.cosmic_bg = np.array([self.solid_angle*efficiency*(87.4*energy**(-2.3)) for efficiency, energy in zip(self.efficiencies, self.energies)])
        return self.cosmic_bg

    def calculate_shield_leakage(self):
        self.shield_leakage = np.array([leaks * np.exp(1-(self.shield_thickness/5)) for leaks in self.shield_leakage_bg_count_rates])
        return self.shield_leakage
    
    def calculate_neutron_spallation_bg(self): # from fig 5
        self.spallation =  np.array([self.rigidity_cut_off * counts for counts in self.energy_counts])
        correction = self.thickness * self.density * self.area / (3.67 * 8800)
        return self.spallation * correction
    
    def calculate_bg(self):
        return self.calculate_shield_leakage() + self.calculate_cosmic_bg() + self.calculate_neutron_spallation_bg()


class Sensitivity():
    def __init__(self, detector_efficiency, energies, background_noise, area, obstime, sigma=3) -> None:
        self.detector_efficiency = detector_efficiency
        self.energies = energies
        self.background_noise = background_noise
        self.area = area
        self.obstime = obstime
        self.sigma = sigma
    
    def calculate_sensitivity(self):
        return np.array([(self.sigma/efficiency) * np.sqrt((4 * bg_noise)/(self.area * self.obstime * energy)) 
                for efficiency, bg_noise, energy in zip(self.detector_efficiency,
                                                        self.background_noise,
                                                        self.energies)])




def main():
    bg_curves = pd.read_csv('bgcurves.csv')
    energies = bg_curves['energy'].values # keV
    mass_attentuation_coefficients = bg_curves['massatt'].values
    background_values = {
        'density' : 5.85, # g/cc
        'shield_thickness' : 10, # cm 
        'mass_attentuation_coefficients' : mass_attentuation_coefficients, 
        'energies' : energies, # keV
        'solid_angle' : 1.4, # sterdaiens
        'shield_leakage_bg_count_rates' : bg_curves['fig8'].values,
        'rigidity_cut_off' : 1.3,  
        'energy_counts' : bg_curves['fig5'].values,
        'thickness': 0.2, # cm
        'area': 5200, # cm^2
    }
    bg_noise = Background(**background_values)
    background = bg_noise.calculate_bg()
    sensitivity_values = {
        'background_noise' : background,
        'detector_efficiency' : bg_noise.efficiencies,
        'energies' : energies, # keV
        'area' : 5200, # cm^2
        'obstime': 0.80 * 48 * 60 * 60,
    }
    sensitivity = Sensitivity(**sensitivity_values)
    sensitivities = sensitivity.calculate_sensitivity()
    fig, ax = plt.subplots()
    ax.plot(energies, sensitivities * 1.6022E-09)
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.show()
    
    
    
if __name__ == '__main__':
    main()
    