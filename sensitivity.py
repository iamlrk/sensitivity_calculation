# based on code written by Anna

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


KEV_TO_ERGS = 1.6022E-09

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
                 area,
                 material) -> None:
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
        self.material = material

    def calculate_efficiency(self):
        self.efficiencies = [1 - np.exp(-_mu*self.density * self.thickness) for _mu in self.mass_attentuation_coefficients]
        return self.efficiencies

    def calculate_cosmic_bg(self):
        self.calculate_efficiency()
        self.cosmic_bg = np.array([self.solid_angle*efficiency*(87.4*energy**(-2.3)) for efficiency, energy in zip(self.efficiencies, self.energies)])
        return self.cosmic_bg
    
    def ploty(self, ax, show_plot=True):
        ax.plot(self.energies, self.cosmic_bg, label=f'{self.material} - Cosmic Background')
        ax.plot(self.energies, self.shield_leakage, label=f'{self.material} - Shield Leakage')
        ax.plot(self.energies, self.spallation, label=f'{self.material} - Neutron Spallation')
        ax.plot(self.energies, self.total_bg, label=f'{self.material} - Total Background')
        ax.legend()
        ax.set_title('Background')
        if show_plot:
            plt.show()
        return ax

    def calculate_shield_leakage(self):
        self.shield_leakage = np.array([leaks * np.exp(1-(self.shield_thickness/5)) for leaks in self.shield_leakage_bg_count_rates])
        return self.shield_leakage
    
    def calculate_neutron_spallation_bg(self): # from fig 5
        self.spallation =  np.array([self.rigidity_cut_off * counts for counts in self.energy_counts])
        correction = self.thickness * self.density * self.area / (3.67 * 8800)
        self.spallation *= correction
        return self.spallation
    
    def calculate_bg(self):
        self.total_bg = self.calculate_shield_leakage() + self.calculate_cosmic_bg() + self.calculate_neutron_spallation_bg()
        return self.total_bg
        


class Sensitivity():
    def __init__(self, detector_efficiency, energies, background_noise, area, obstime, material, sigma=3, units='kev') -> None:
        self.detector_efficiency = detector_efficiency
        self.energies = energies
        self.background_noise = background_noise
        self.area = area
        self.obstime = obstime
        self.sigma = sigma
        self.material = material
    
    def ploty(self, ax, show_plot=True):
        ax.plot(self.energies, self.sensitivities * 1.4**2, label=f'{self.material}Sensitivity') # KEV_TO_ERGS)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title('Sensitivity Plot')
        ax.grid()
        ax.legend()
        if show_plot:
            plt.show()
        return ax
    
    def calculate_sensitivity(self):
        self.sensitivities =  np.array([(self.sigma/efficiency) * np.sqrt((4 * bg_noise)/(self.area * self.obstime * energy)) 
                            for efficiency, bg_noise, energy in zip(self.detector_efficiency,
                                                                    self.background_noise,
                                                                    self.energies)])
        return self.sensitivities




def ourmission():
    bg_curves = pd.read_csv('bgcurves.csv')
    energies = bg_curves['energy'].values # keV
    mass_attentuation_coefficients = bg_curves['massatt'].values
    cdte_background_values = {
        'density' : 5.85, # g/cc
        'shield_thickness' : 10, # cm 
        'mass_attentuation_coefficients' : mass_attentuation_coefficients, 
        'energies' : energies, # keV
        'solid_angle' : 0.7, # steradians
        'shield_leakage_bg_count_rates' : bg_curves['fig8'].values,
        'rigidity_cut_off' : 1.3,  
        'energy_counts' : bg_curves['fig5'].values,
        'thickness': 0.2, # cm
        'area': 3466.88, # cm^2
        'material': 'CdTe',
    }
    csi_background_values = {
        'density' : 4.51, # g/cc
        'shield_thickness' : 10, # cm 
        'mass_attentuation_coefficients' : mass_attentuation_coefficients, 
        'energies' : energies, # keV
        'solid_angle' : 0.7, # sterdaiens
        'shield_leakage_bg_count_rates' : bg_curves['fig8'].values,
        'rigidity_cut_off' : 1.3,  
        'energy_counts' : bg_curves['fig5'].values,
        'thickness': 0.2, # cm
        'area': 3466.88, # cm^2
        'material': 'CsI',
    }
    
    cdte_bg_noise = Background(**cdte_background_values)
    cdte_background = cdte_bg_noise.calculate_bg()
    # fig, ax = plt.subplots()
    # ax = cdte_bg_noise.ploty(ax, show_plot=False)
    
    csi_bg_noise = Background(**csi_background_values)
    csi_background = csi_bg_noise.calculate_bg()
    # fig, ax = plt.subplots()
    # ax = csi_bg_noise.ploty(ax, show_plot=False)
    
    # plt.show()
    
    cdte_sensitivity_values = {
        'background_noise' : cdte_background,
        'detector_efficiency' : cdte_bg_noise.efficiencies,
        'energies' : energies, # keV
        'area' : 3466.85, # cm^2
        'obstime': 0.87 * 48 * 60 * 60,
        'material': 'CdTe',

    }
    cdte_sensitivity = Sensitivity(**cdte_sensitivity_values)
    cdte_sensitivities = cdte_sensitivity.calculate_sensitivity()
    snsfig, snsax = plt.subplots()
    # snsax = cdte_sensitivity.ploty(snsax, show_plot=False)
 
    csi_sensitivity_values = {
        'background_noise' : csi_background,
        'detector_efficiency' : cdte_bg_noise.efficiencies,
        'energies' : energies, # keV
        'area' : 3466.85, # cm^2
        'obstime': 0.87 * 48 * 60 * 60,
        'material': 'CsI',
    }
    csi_sensitivity = Sensitivity(**csi_sensitivity_values)
    csi_sensitivities = csi_sensitivity.calculate_sensitivity()
    # snsfig, snsax = plt.subplots()
    snsax = csi_sensitivity.ploty(snsax, show_plot=False)
    plt.show()
      
    
def bat():
    bat_bg_curves = pd.read_csv('batbgcurves.csv')
    bat_energies = bat_bg_curves['energy'].values # keV
    bat_mass_attentuation_coefficients = bat_bg_curves['massatt'].values
    bat_background_values = {
        'density' : 5.76, # g/cc
        'shield_thickness' : 10, # cm 
        'mass_attentuation_coefficients' : bat_mass_attentuation_coefficients, 
        'energies' : bat_energies, # keV
        'solid_angle' : 1.4, # sterdaiens
        'shield_leakage_bg_count_rates' : bat_bg_curves['fig8'].values,
        'rigidity_cut_off' : 1.3,  
        'energy_counts' : bat_bg_curves['fig5'].values,
        'thickness': 0.2, # cm
        'area': 5200, # cm^2
    }
    bat_bg_noise = Background(**bat_background_values)
    bat_background = bat_bg_noise.calculate_bg()
    # batfig, batax = plt.subplots()
    # dd = bat_bg_noise.ploty(batax, show_plot=False)
    
    bat_sensitivity_values = {
        'background_noise' : bat_background,
        'detector_efficiency' : bat_bg_noise.efficiencies,
        'energies' : bat_energies, # keV
        'area' : 5200, # cm^2
        'obstime': 0.87 * 48 * 60 * 60,
    }
    bat_sensitivity = Sensitivity(**bat_sensitivity_values)
    bat_sensitivities = bat_sensitivity.calculate_sensitivity()
    fig, ax = plt.subplots()
    ax = bat_sensitivity.ploty(ax, show_plot=False)
    ax.set_xlim(-10, 1e3)
    ax.set_ylim(1e-5, 10)
    plt.show()
    
if __name__ == '__main__':
    ourmission()
    
