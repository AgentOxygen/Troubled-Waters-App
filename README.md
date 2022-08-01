# Troubled Waters App
I will use Flask to host a webpage with a MapBox integration. Data originates from netcdf files found in '/netcdf' and is handled differently between
the development and production versions of the app. The GUI should remain the same between both versions with the exception of default settings which
may change frequenty in development but not in production.

## Development Version
Flask will serve as the primary backend for all data handling. I will pull data directly from xarray DataArrays, preloaded at the start of the Flask server,
and then apply shapefile masks in real time to obtain values. This will allow for rapid prototyping and testing of various metric calculations and visualization
features. This also comes at the cost of performance and will likely only allow for a few active users at a time.

## Production Version (TBD)
Flask will host the webpage and all HTML GET/PUSH requests while Redis will handle the data backend. All metrics should be calculated beforehand and uploaded
to the Redis database. This drastically cut down on overhead in comparison to development. I will use Kubernetes to create services for Redis and Flask with pods
that handle the GET/PUSH requests. This should provide some reliability in the webapp that guards against bugs and errors. I will also create system for keeping
a centralized log of any errors that occur. Finally, I will containerize this project in Docker for greater portability.

### /netcdf
Contains all the original netcdf files from the California Hydroclimate project

### /development
Contains all files and directories relevant to the development version of the app