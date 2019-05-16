- Pillco Zolá et al., 2019: Modelling Lake Titicaca's daily and monthly evaporation (https://doi.org/10.5194/hess-23-657-2019)
  - Paper on Lake Titicaca water balance, I used monthly averages of water surface temp. observed during the 2015–2016 period (Table 3) for SST_update files    // Evgeny

- Gálvez et al., 2005: The WRF model as a tool to understand mesoscale processes on the poorly sampled South American Altiplano (https://ams.confex.com/ams/32Rad11Meso/webprogram/Paper97415.html)
  - Extended abstract for 11th Conference on Mesoscale Processes (AMS) on modelling Altiplano region with WRF focusing mesoscale circulations and rainfall patterns. I couldn't find any peer-reviewed papers and NOAA's project site seems to be down (http://www.nssl.noaa.gov/projects/pacs/web/ALTIPLANO/NF/)(*). Anyway authors disclosed and fixed revealed boundary condition problems (Lake Titicaca surf. temp.) in default WRF and demonstrated model improvements. More links here: http://josemanuelgalvez.net/    // Evgeny
  - trial simulation reveal that 1km resolution better reproduce storms at TTCC lake // diego 
  - unnusual low land-surface temperatures around the lake are reported. they affected "the structure of the circulations and associated convection" duting the day // diego 
  - Link (*) seems to be here now: https://www.eol.ucar.edu/field_projects/salljex //Diego
  
- Norris, J. et al.: The spatiotemporal variability of precipitation over the Himalaya: evaluation of one-year WRF model simulation. Climate Dynamics 49, 2179–2204 (2017).
  - 1 year simulation with spectral nudginng in the outter domain //diego 
  - resolution 6.2 km for inner domain // diego
 
 
- Wang, W. NCAR/NESL/MMM January 2014. 38
  - SST is indeed used for long simulations (pp 11) as it allows control of sea ice, monthly vegetation fraction, albedo.  // diego
  - I wonder if we should look into the other options for long simulations pp. 12 // diego 
  
- Ma, Y. et al. Comparison of Analysis and Spectral Nudging Techniques for Dynamical Downscaling with the WRF Model over China. Advances in Meteorology 17
  - regarding spectral vs analysis (grid) nudging they conclude: "Compared with observations, the results show that both of the nudging experiments decrease the bias of conventional meteorological elements near the surface and at different heights during the process of dynamical downscaling. However, spectral nudging outperforms analysis nudging for predicting precipitation, and analysis nudging outperforms spectral nudging for the simulation of air humidity and wind speed". Since we are interested in wind I guess its safe to stick to grid nudging // diego 

- Recent papers on WRF model PBL schemes // Evgeny
  - Avolio et al., 2017: Sensitivity analysis of WRF model PBL schemes in simulating boundary-layer variables in southern Italy: An experimental campaign (https://doi.org/10.1016/j.atmosres.2017.04.003).
    - 5 different WRF PBLs vs Measurement campain (surface station and meteo.mast + Lidar and Sodar + ceilometer) in Calabria region (southern Italy)
  - Banks et al., 2017: Sensitivity of boundary-layer variables to PBL schemes in the WRF modelbased on surface meteorological observations, lidar, and radiosondesduring the HygrA-CD campaign (https://doi.org/10.1016/j.atmosres.2016.02.024).
    - 8 different WRF PBLs vs multiple meteorological stations, multiwavelength Raman lidar, radiosonde launches over the complex, urban terrain of the Greater Athens Area
  - Banks et al., 2015: Performance Evaluation of the Boundary-Layer Height from Lidar and the Weather Research and Forecasting Model at an Urban Coastal Site in the North-East Iberian Peninsula (https://doi.org/10.1007/s10546-015-0056-2).
    - 8 different WRF PBLs over Iberian Peninsula; three-day back-trajectories cluster analysis algorithm for a 16-year period over Barcelona; PBL heights are validated against lidar estimates: ACM2 is the most reliable, with the widely-tested MYJ (we are using it) showing the weakest correlations with lidar retrievals
  - ACM2 scheme showed the best results in all 3 papers.
