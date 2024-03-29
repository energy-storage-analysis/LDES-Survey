# Kale 2018

[Kale, V., et al. 2018. A comparative study between optimal metal and composite rotors for flywheel energy storage systems. Energy Reports 4, 576–585.](https://doi.org/10/gm8c9v)


This publication contains allowed stresses ($\sigma_A$) and mass densities ($\rho_m$) of isotropic and composite materials. These data are used to calculate the specific strength of these materials, $\sigma_A/\rho_m$. 

This data is the primary source of the materials define the Virial-limited storage media (pressure tanks, SMES, and Flywheels). These different storage media are created during data processing as near-duplicates except for different $Q_{max}$ which depends on the geometry of the system. The $Q_{max}$ for the different types are determined from [Nomura, et al. “Structural Limitations of Energy Storage Systems Based on the Virial Theorem.” IEEE Transactions on Applied Superconductivity, Vol. 27, No. 4, 2017](https://doi.org/10/gjg4k7).

For isotropic materials (Table A1) $\sigma_A$ is taken as the yield strength. For composite materials (Table A2) the highest ultimate hoop stress is used, which is given by the variable $\sigma^{ult}_T$ in the paper.  

Prices of materials are also given in relative terms, normalized to "the cost of the cheapest material in the evaluated set of materials." This appears to be Steel-4340, but no absolute price is given. We use the price of steel obtained from other sources for this base price to calculate the absolute prices of other materials. Prices are grouped into larger material categories (see mat_lookup.csv). The output price of steel is dropped to not be included in the final material dataset and cause a feedback loop. 

## Development: 

## Determining meaning of acronyms
### CRFP: carbon fiber reinforced plastic

I think carbon fibers with an epoxy materx are CRFP, i.e. the plastic can also mean 'epoxy'. Like this

https://www.matweb.com/search/datasheettext.aspx?matguid=2b1eb4b94183474eb0aab2cf855b3b56


https://asmedigitalcollection.asme.org/materialstechnology/article-abstract/112/1/61/402447/Mechanical-Characterization-of-IM7-8551-7-Carbon?redirectedFrom=fulltext

> IM7 is a high elongation, high strength carbon fiber, and the 8551-7 matrix is a high toughness epoxy resin.



T300 is a carbon fiber

https://www.rockwestcomposites.com/media/wysiwyg/T300DataSheet_1.pdf
### GRE




Glass Reinforced Epoxy (GRE)
https://www.corrosionpedia.com/definition/6781/glass-reinforced-epoxy-gre


 ### KFRP

 Kevlar (aramid) fiber reinforced polymers

 http://www.substech.com/dokuwiki/doku.php?id=kevlar_aramid_fiber_reinforced_polymers