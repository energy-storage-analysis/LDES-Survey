

# Combination Storage Media

This section derives some basic forumulas for the overall energy capital cost, $C_{kWh}$ of a energy storage system using multiple storage media or multiple forms of energy from one storage media. This is not intended to be a comprehensive list of all possiblities of types of energy storage systems but provide some formulas that can be used with the data presented in the paper to estimate the energy capital of some simple classes of composite storage media. Beyond this level of complexity, a more complete analysis taking into account the efficiency and power conversion system would likely be needed for any valubale insight. 

In any case, $C_{kWh}$ can be calculated from 

$$ C_{kWh} = \frac{C_{tot}}{Cap_E} $$

Where $C_{tot} [USD]$ is the total cost of the entire energy storage system, and $Cap_E[kWh]$ is the total energy capacity of the energy storage system. 

## Multiple storage media

![Figure 1: An energy storage system comprised of multiple storage media](../../SI_docs//figures/output/composite_SM_serial.png)

We consider a energy storage system comprised of multiple storage media (indexed by $i$) each contributing and energy capacity  a fraction $f_i$ of Cap_E. Each storage medium has a specific cost $C_{mat,i}$ and mass $M_i$. 

$$  C_{kWh} = \frac{\sum_i{C_{mat, i}M_i}}{Cap_E} $$

$$ C_{kWh} = \sum_i\frac{{C_{mat, i}}}{Cap_E/M_i} $$

Using the fact that $Cap_E = Cap_{E,i}/f_i$ and $\rho_{E,i} = Cap_{E,i}/M_i$

$$ C_{kWh} = \sum_i f_i \frac{{C_{mat, i}}}{\rho_{E,i}} $$

$$ C_{kWh} = \sum_i f_i C_{kWh,i}$$

Therefore, the overall energy capital cost is an energy-weighted mean of the individual energy capital costs. 

## Multiple forms of energy from one material


![Figure 2: An energy storage system comprised of one storage media containing multiple forms of energy](../../SI_docs/figures/output/composite_SM_parallel.png)

We now look at the case where multiple forms of energy are stored in the same material. 

$$ C_{kWh} = \frac{C_{mat}M}{\sum_if_iCap_{E,i}} $$

$$ C_{kWh} = \frac{1}{\sum_i \frac{f_iCap_{E,i}}{C_{mat}M}} $$

$$ C_{kWh} = \frac{1}{\sum_i \frac{f_i}{C_{kWh,i}}} $$

Therefore, the overall energy capital cost is an energy-weighted harmonic mean of the individual energy capital costs. 

## Matched Sensible Thermal storage


In the case of pumped thermal storage both a hot and cold storage media are required, which are generally required to have matched energy capacities as heat is transfered between the two to charge and discharge the energy. 

![Figure 3: An energy storage system comprised energy-matched hot and cold sensible thermal storage media](../../SI_docs/figures/output/composite_SM_thermal.png)

$$ Cap_E = Q = M_H C_{P,H}\Delta T_H = M_C C_{P,C}\Delta T_C $$

$$ C_{kWh} = \frac{C_{mat,H}M_H + C_{mat,C}M_C }{Q}$$

$$ C_{kWh} = \frac{C_{mat,H}}{C_{P,H}\Delta T_H} + \frac{C_{mat,C}}{C_{P,C}\Delta T_C} $$
$$ C_{kWh} = C_{kWh,H} + C_{kWh,C}$$

Therefore the fact that more of a storage medium with smaller $\Delta T$ is needed is already taken into account when adding togher the energy capital costs of each storage medium. 


