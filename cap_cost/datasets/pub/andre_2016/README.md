Thermochemical material physical data

André, L., Abanades, S., Flamant, G., 2016. Screening of thermochemical systems based on solid-gas reversible reactions for high temperature solar thermal energy storage. Renewable and Sustainable Energy Reviews 64, 703–715. https://doi.org/10.1016/j.rser.2016.06.043

The materials selection were chosen based on what seemed generally more common and is in the price database. This seems valid as the whole point is a reversible transformation between the two. 

## Development

TODO: There are a few 'fudged' (but probably close enough) materials selections. 
* Zn for ZnO
* MnO2 for MnO (and other Mn oxides)

The mat_type is also extracted from the tables so is not in the SM_lookup making things inconsistent. Is there a better way to handle this case? If it is in both then you get two columns "mat_type_x" and "mat_type_y". It looks like the normal way to merge with overwriting is `combine_first` but this would change the code consistency. Just deleting mat_type from the lookup for now