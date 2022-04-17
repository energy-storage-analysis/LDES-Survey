import numpy as np
import xyzpy

#4380 max cycles following Albertus
@xyzpy.label(var_names=['CF'])
def calc_CF(num_cycles_year, DD):
    """
    Calculates the capacity factor from #/cycles/year and discharge duration
    """
    CF = num_cycles_year*(DD/4380)
    if CF > 1:
        return np.nan
    else:
        return CF

@xyzpy.label(var_names=['DD'])
def calc_DD_from_CF(num_cycles_year, CF):
    """
    Calculates discharge duraiton from num_cycles_year and CF 
    """
    DD = CF*(4380/num_cycles_year)
    return DD


@xyzpy.label(var_names=['lcos'])
def calc_lcos(DD, CF, C_Ein, eta_RT, C_kW, C_kWh, LT):
    """
    The main equation for LCOS
    """
    elec_premium = C_Ein*((1/eta_RT)-1)

    capital_term_dem = C_kW + C_kWh*DD
    capital_term_num = LT*4380*CF*np.sqrt(eta_RT) 
    capital_term = capital_term_dem/capital_term_num

    lcos= elec_premium + capital_term
    return lcos

@xyzpy.label(var_names=['lcos'])
def calc_lcos_ncy(DD, num_cycles_year, C_Ein, eta_RT, C_kW, C_kWh, LT):
    """
    A wrapper for LCOS with internal CF calculation
    """
    CF = calc_CF(num_cycles_year, DD)
    lcos = calc_lcos(DD, CF, C_Ein, eta_RT, C_kW, C_kWh, LT)
    return lcos

@xyzpy.label(var_names=['C_kW'])
def calc_CkW_max(DD, C_kWh, eta_RT, LT, CF, C_Ein, LCOS_set):
    """
    Calcualtion of maximum CkW given LCOS target and other parameters (Albertus plot) 
    """
    eta_d = np.sqrt(eta_RT)
    C_kW = LT*4380*CF*eta_d*( LCOS_set - ( (1/eta_RT)-1 )*C_Ein ) - C_kWh*DD
    return C_kW