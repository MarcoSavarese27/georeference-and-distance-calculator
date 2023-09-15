# georeference-and-distance-calculator
Backend of a web application that collects geographic datas of a limited set of locations and calculates the distance between them.<br>
The app is divided in two microservices:<br>
- Georeference: interacting with ArcGis, the app returns the geolocalisation of a given set of addresses;
- Distance Calculator and Distance Matrix: interacting with OSRM, with the georeferenced addresses, the software calculates the distance and the time between them and puts all the results in a matrix.

Supported inputs:
 - JSON
 - .xlsx

Supported outputs:
- JSON
- .xlsx

The user may retrieve data in three ways:
- ID: returns a uuid. This uuid can be used as a handle: the user, by doing a get with this id, can retrieve datas. If the resource is not ready, the user will wait for the process to end;
- URL: similar to the ID method, the code returns an URL. The user may use the URL to retrieve the datas;
- Inline: direct response. 
