# hec-python
Python code for senior HID project: connecting morphology and oxbow sedimentation

## Data Dependencies
 - HDF file from HEC-RAS output
 - Binary raster showing where river channel is and basin extent 
 - Trinity river gage data (https://waterdata.usgs.gov/ca/nwis/uv?site_no=11530000)

## Scripts 
 - read_hdf5.py: code for reading a .hdf file and plotting output
 - terrain_mod.py: code for reading a binary raster file that shows where the river channel is and adding appropriate basin slopes (linear from top to bottom, polynomial from side to side)
 - trinity_gage_read.py: code for reading Trinity river gage data (not used/important) 

## Python Dependencies
 - h5py
 - matplotlib
 - pandas
 - numpy 
 - scipy
 - netCDF4