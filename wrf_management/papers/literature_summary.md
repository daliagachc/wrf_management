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


