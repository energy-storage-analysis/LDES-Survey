[Southall, E. et al. “Analysis of Liquid Organic Hydrogen Carrier Systems.” Johnson Matthey Technology Review, 2022](https://doi.org/10.1595/205651322X16415722152530).

This publication contains physical property and material price data for liquid organic hydrogen carriers (LOHC). The data from table 1 were pulled manually to form material prices. The weight percent of hydrogen ($ W_{H_2} $) is used to calculate the overall Gibbs free energy per  mole of host molecule. 

$$ \Delta G [\frac{kWh}{mol_{host}}] = \Delta G[\frac{kWh}{mol_{H_2}}] \times r_{H_2} $$

$$ r_{H_2} = \frac{W_{H_2} \mu_{host}}{(1-W_{H_2}) \mu_{H_2}}$$

Molecular formulas taken from Modisha 2019

## Development

TODO: Currently the enthalpy of dehydrogenation is not taken into account and probably should be subtracted from the hydrogen gas Gibbs energy. This could be handled similarly to Hurskainen 2020 Table 3. 