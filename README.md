# Troubled Waters App
I will use Flask to host a webpage with a MapBox integration. Data originates from netcdf files found in '/netcdf' and is handled differently between
the development and production versions of the app. The GUI should remain the same between both versions with the exception of default settings which
may change frequenty in development but not in production.

## Flask Version
Flask serves as the primary backend for all data handling. Data is pulled directly from xarray DataArrays, preloaded at the start of the Flask server,
and then apply shapefile masks in real time to obtain values. This allows for rapid prototyping and testing of various metric calculations and visualization
features. This also comes at the cost of performance and will likely only allow for a few active users at a time.

## Development Version
Here, I switch from Flask to Node.js and from Redis to PostgreSQL. Both of these are more scalable and will likely be easier to utilize in production. Later, I will implement kubernetes.

### /netcdf
Contains all the original netcdf files from the California Hydroclimate project

### /development
Contains all files and directories relevant to the development version of the app