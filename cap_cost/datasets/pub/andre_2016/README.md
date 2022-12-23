# Andre 2016

[André, L. et al. 2016. Screening of thermochemical systems based on solid-gas reversible reactions for high temperature solar thermal energy storage. Renewable and Sustainable Energy Reviews 64, 703–715 ](https://doi.org/10.1016/j.rser.2016.06.043)

This work performed an extensive search of thermochemical materials for high temperature thermal storage based on physical considerations (not cost) and that is our primary data source for thermochemical storage media. The dataset includes tabular physical property data for metal oxides, sulphates, carbonates, and hydrates that undergo thermal decomposition reactions at high temperature relevant to high-temperature thermal storage.

The materials are specified in the paeper as "product/reactant" (e.g. Ca(OH)2/CaO). The material assignment was based on either the product or reactant based on which form generally appeared more common and/or prices could be found for it. This approach is justified as the charging/discharging process is a reversible transformation between the two materials. 

## Development

TODO: There are a few 'fudged' (but probably close enough) materials selections. 
* Zn for ZnO
* MnO2 for MnO (and other Mn oxides)

The mat_type is extracted from the tables, and is therefore is not in the SM_lookup making things inconsistent. Is there a better way to handle this case? If it is in both then you get two columns "mat_type_x" and "mat_type_y". It looks like the normal way to merge with overwriting is `combine_first` but this would change the code consistency. Just deleting mat_type from the lookup for now