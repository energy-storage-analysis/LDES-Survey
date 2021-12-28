#%%
from dataclasses import dataclass
import csv
from scipy.constants import physical_constants
from pint import Quantity

def const_to_pint(phys_const):
    return Quantity(phys_const[0], phys_const[1])


F = const_to_pint(physical_constants['Faraday constant'])
e = const_to_pint(physical_constants['elementary charge'])
M_nuc = const_to_pint(physical_constants['neutron mass'])
mu_0 = const_to_pint(physical_constants['vacuum mag. permeability'])
g = Quantity(9.8, 'm/s**2')


#%%
@dataclass(kw_only=True)
class StorageMedium:
    rho_m: float = None
    name: str = ''

@dataclass(kw_only=True)
class Transformation:
    SAV: float = None
    rho_m: float = None
    name:str = ''

@dataclass
class Device:
    storage_medium: StorageMedium
    transformation: Transformation
    name: str = ''

    def ragone_coords(self):
        return (
            self.storage_medium.energy_density,
            self.transformation.power_flux
        )


## Storage Media
@dataclass
class ThermalEnergy(StorageMedium):
    deltaT: float
    C_p: float

    @property 
    def energy_density(self):
        return self.C_p*self.deltaT


@dataclass
class VirialLimited(StorageMedium):
    sigma_a: float
    Q_max: float = 1

    @property 
    def energy_density(self):
        return self.sigma_a/(self.Q_max*self.rho_m)


@dataclass
class ChemicalEnergy(StorageMedium):
    """
    Chemical Energy density defined through electrochemical reaction

    args: 
        deltaV: Bond Voltage Difference
        n_e: Number electrons involved electrons
        f_active: Active component mass fraction
        M_mol: Molar Mass of active components
    """
    deltaV: float
    n_e: int
    f_active: float
    M_mol: float

    @property
    def energy_density(self):
        return F*self.deltaV*self.n_e*self.f_active/self.M_mol

@dataclass
class GravitationalEnergy(StorageMedium):
    deltaH: float

    @property
    def energy_density(self):
        return self.deltaH*g

@dataclass
class ECDiffusion(Transformation):
    deltaV: float
    c_b: float
    D: float
    l: float

    @property
    def power_flux(self):
        return F*self.deltaV*self.c_b*self.D/self.l
@dataclass
class ThermoMechanical(Transformation):
    """
    Thermomechanical transformation

    args: 
        deltaP: Turbine Pressure Differential (Pa)
    """
    deltaP: float 
    velocity: float

    @property
    def power_flux(self):
        return self.deltaP*self.velocity

@dataclass
class Mechanical(Transformation):
    B: float
    velocity: float = Quantity(100, 'm/s')

    @property
    def power_flux(self):
        return self.velocity*self.B**2/(2*mu_0)


@dataclass
class Inverter(Transformation):

    @property
    def power_flux(self):
        return Quantity(1e11, 'W/m^2') #TODO: formula?

te_500K = ThermalEnergy(
    rho_m = Quantity(1, 'kg/L'), 
    deltaT=Quantity(500,'K'), 
    C_p=Quantity(1, 'kJ/kg/K')
    )

VTsteel = VirialLimited(
    rho_m = Quantity(8, 'kg/L'), 
    sigma_a= Quantity(400, 'MPa')
    )

hydrocarbon = ChemicalEnergy(
    deltaV=Quantity(1, 'V'),
    n_e=4,
    f_active=1,
    M_mol = Quantity(14, 'g/mol'),
    rho_m=Quantity(0.7, 'kg/L')
)

lib_elec = ChemicalEnergy(
    deltaV=Quantity(3, 'V'),
    n_e=1,
    f_active=0.02,
    M_mol = Quantity(3, 'g/mol'),
    rho_m=Quantity(1, 'kg/L')
)

#TODO: calculate for whole aqueous solution. How to handle cost calculation later on?
vanadium_soln = ChemicalEnergy(
    deltaV=Quantity(1, 'V'),
    n_e=1,
    f_active=0.01, 
    M_mol = Quantity(18, 'g/mol'),
    rho_m=Quantity(1, 'kg/L')
)

diff_gdl = ECDiffusion(
    Quantity(1, 'V'), 
    Quantity(1e-5, 'mol/cm^3'), 
    Quantity(1e-1, 'cm^2/s'), 
    Quantity(1e-2, 'cm')
    )

diff_aq = ECDiffusion(
    Quantity(1, 'V'), 
    Quantity(1e-3, 'mol/cm^3'), 
    Quantity(1e-6, 'cm^2/s'), 
    Quantity(1e-3, 'cm')
    )

diff_li = ECDiffusion(
    Quantity(3, 'V'), 
    Quantity(1e-3, 'mol/cm^3'), 
    Quantity(1e-7, 'cm^2/s'), 
    Quantity(1e-2, 'cm')
    )

gt = ThermoMechanical(
    deltaP = Quantity(1e6, 'Pa'),
    velocity = Quantity(100, 'm/s')
    )

motor = Mechanical(B = Quantity(1,'T'))

devices = {
    'ptes' : Device(
        name='Pumped Thermal Energy Storage',
        storage_medium=te_500K,
        transformation=gt
    ),
    'rfc': Device(
        name='Fuel Cell/Electrolysis',
        storage_medium=hydrocarbon,
        transformation=diff_gdl
    ),
    'conv_power': Device(
        name='Combined Cycle Power Generation',
        storage_medium=hydrocarbon,
        transformation=gt
    ),
    'caes': Device(
        name='Diabatic/Isothermal Compressed Air',
        storage_medium=VTsteel,
        transformation=gt
    ),
    'vrfb': Device(
        name='Vanadium Redox Flow Battery',
        storage_medium=vanadium_soln,
        transformation=diff_aq
    ),
    'flywheel': Device(
        name='Flywheel Energy Storage',
        storage_medium=VTsteel,
        transformation=motor
    ),
    'phes': Device(
        name='Pumped Hydro',
        storage_medium=GravitationalEnergy(
            rho_m=Quantity(1, 'kg/L'),
            deltaH=Quantity(100,'m')
        ),
        transformation=motor
    ),
    'lib': Device(
        name='Lithium Ion Battery',
        storage_medium=lib_elec,
        transformation=diff_li
    ),
    'smes': Device(
        name='Superconducting Magnetic',
        storage_medium=VTsteel,
        transformation= Inverter()
    )
}

# %%
