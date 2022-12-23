# Calculation methods

## Hydrogen carrier energy density calculation method

We calculate the specific energy density of hydrogen carriers from the theoretical weight percentage of molecular hydrogen in the host material, $C_{wt.\%}$:

$$ C_{wt.\%} = \frac{r_{H_2}\mu_{H_2}}{\mu_{host} + r_{H_2}\mu_{H_2}} $$

Where $\mu_{H_2}$ and $\mu_{host}$ are the molar masses of molecular hydrogen and the host material, repectively. $r_{H_2} = \frac{N_{H_2}}{N_{Host}}$ is the ratio of the moles of molecular hydrogen to the moles of the host material. Note that because $r_{H_2}\mu_{H_2} = r_{H}\mu_H$ it doesn't matter if the weight percentage is expessed in terms of $H$ or $H_2$. 

We then solve for $r_{H_2}$, 

$$ r_{H_2} = \frac{ C_{wt.\%} * \mu_{host}} {(1- C_{wt.\%}) * \mu_{H_2}}, $$

which can then be used to calculate the Gibbs free energy per mole of the host material, $\Delta G_{host}$

$$ \Delta G [\frac{kWh}{mol_{host}}] = \Delta G[\frac{kWh}{mol_{H_2}}] \times r_{H_2} $$

Where $\Delta G_{H_2} = 0.0659 kWh/mol$

which is later converted to a specifc energy density with the molar mass of the host, alongside other chemical energy calculations. 