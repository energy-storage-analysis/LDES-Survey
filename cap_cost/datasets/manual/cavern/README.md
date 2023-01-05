# Underground Cavern Storage 

This dataset defines storage media that store energy through a pressurized gas in undergound caverns. This includes storage of pressure energy in the form of compressed air as well as the storage of chemical energy as a pressurized methane or hydrogen gas. For both of these types of storage media the same volumetric cavern costs are used to calculate the specific energy density. 

Here, the mass density of each gas ($\rho_m$) is calculated assuming a cavern pressure of $P$ through the equation 

$$ \rho_m = \frac{\mu P}{RT}$$

Where $\mu$ is the molar mass of the gas, $R$ the ideal gas constant,  and $T = 330K$. 

$\rho_m$ is used with a volumetric costs ($USD/m^3$) deterimed for underground salt caverns and lined rock caverns (LRC) through three datasets, Papadias 2021, Lord 2014, and ETI 2018.The datasets are limited to those that provide marginal volumetric construction costs as much as possible. This is difficult as the exact definition of the cost components in the sources is not always clear and some amount of fixed capital costs are included in their voumetric cost components (e.g salt leeching plant capital costs). The methodology for determining the volumetric costs for Salt Caverns and Lined Rock Caverns is outlined below, and some source-specific processing steps are outlined in the source's indiviual readme files. 

For both types of caverns a gas pressure of 1e7 Pa is assumed. The speicifc price of different combinations of caverns and working gas is calculated from the volumetric cost and the mass density of different gasses at this pressure. We note that Lord 2014 cautions against this, as hydrogen will have significantly different design requriements than other gasses relevant to pressurized gas stoarage (e.g. CO2, N2). This methodology represents a rough estimate allowing for comparision of underground chemical energy storage and pressurized energy storage on a consistent basis.  

## Salt caverns: 

We attempted to obtain the the volumetric cost of leeching a salt cavern without fixed leeching plant capital costs. Lord 2014 breaks out salt cavern construction costs into mining costs (USD/m^3) and Leaching plant costs (USD). The leaching plant costs are converted to a volumetric basis with the cavern void volume in Table 1 which allows for the calculation of an mining cost fraction, which represents the approximate fraction of volumetric leaching costs over the overall leaching capital cost.

mining cost fraction = (mining cost)/(mining cost + volumetric leaching plant cost) = 0.5715509854327335

This fraction is appied to both Papadias 2021 and ETI 2018 which appear to included fixed capital costs as well as volumetric leaching costs, which are assumed to be approximately the same as the leaching plant cost mentioned above: 

ETI: "The creation of salt cavern stores through drilling of wells into the salt layer and leaching 
of a void including supporting process equipment such as brine pipework, pumps etc. "

For Papadias the salt cavern leaching costs decrease with increasing "Cavern Roof Depth" which indicates a fixed cost component. The leaching costs for the 2000 ft cavern are used for a target pressure of 100 atm. 

## Lined Rock Cavern: 
We attempted to obtain the the volumetric cost of dome formation without cavern liner, as the cost contribution of the cavern liner would in prinicple decrease with cavern size. 

Papadias 2021 indicates the dome constructions costs, which are used. Lord 2014 indicates the "Mining costs" with units of USD/m^3 which are assumed to be approximately the dome construction costs. 

## Development

TODO: Perhaps a similar fraction based analysis could be used from the ETI data, to include the salt cavern data from Kruck, which includes "Exploration, drilling, leaching,first fill". ETI also includes data for "MIT's, Run completions & 1st Gas fills ", which is ignored for now. 

HDSAM contains a geologic cavern cost scaling relationship that could be included here. 