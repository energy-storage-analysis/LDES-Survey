# Antunez 2018

[Antunez, P. F. Modelling and Development of Thermo-Mechanical Energy Storage. University of Cambridge, 2018.](https://www.repository.cam.ac.uk/handle/1810/290867)

This PhD thesis includes physical properties and cost data of sensible thermal storage including cold storage media. This dataset is extracted from Table 1.1. 

The Liquid Air datapoint is taken from the the specific exergy given in section 3.2.1. We classify liquid air as a latent heat storage medium for simplicity and integration into our analysis. However, this is technically inaccurate as the exergy value is a complex function of the 'steady flow availablility' which also includes the sensible heat extraction bringing the gaseous air to ambient conditions, and might be more accurately classified as a combination latent and sensible storage medium. We use the volumetric costs for cryogenic storage of LNG following a [report by Highview Power](https://www.highviewpower.com/wp-content/uploads/2018/04/Highview-Brochure-November-2017-Online-A4-web.pdf) indicating that cryogenic storage for LAES systems can utilize experience with LNG storage.   

## Development

I couldn't get the tabula template to work properly, which I think has to do with the fact that the table is rotated but there is still regular text on the page. Adding rotate extract setting to 90 was needed but not sufficient. I had to manually swap x2 and y2 in the tabula_template.json (and dial them in a bit). 

TODO: I added a extration keword to do this now ('table_rotate'), but it's hacky and nees to be revisted. See extract_dfs function. 