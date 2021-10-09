# COVID dashboard Poland
A small project which aim is to present on a interactive dashboard with COVID data in Poland

## Interctive map
https://covid-dashboard-poland.herokuapp.com/

## Geo data sources
1. [The Main Office of Geodesy and Cartography regional division of the country into municipalities (shapefile)](http://www.gugik.gov.pl/pzgik/dane-bez-oplat/dane-z-panstwowego-rejestru-granic-i-powierzchni-jednostek-podzialow-terytorialnych-kraju-prg)

## Covid data sources
1. [Official COVID vaccination data from "Open data" portal](https://dane.gov.pl/pl/dataset/2476)
2. [Official COVID data from "Open data" portal](https://dane.gov.pl/en/dataset/2477)

## Authors
Sebastian Konicz - sebastian.konicz@gmail.com

## Project Organization

------------

    ├── data                            <- place whre the data is stored
    │   │
    │   ├── final                           <- final files
	│   │
    │   ├── geo                             <- geospatial data
    │   │
    │   ├── interim                         <- intermediate data that has been transformed
    │   │
    │   └── raw                             <- the original, immutable data dump
    │
    ├── src                             <- source code for use in this project
    │   │
    │   ├── diss                                <- dissregarted scripts
    │   │
    │   ├── 001_map_to_geojson.py               <- crates geojson files form geospacial data (shp)
    │   │
    │   ├── 002_vac_cou_data_load.py            <- creates one dataframe from official vaccination data
    │   │
    │   ├── 003_cov_data_load.py                <- creates one dataframe from official covid dataa
    │   │
    │   └── 101_cov_data_transformation.py      <- transform covid data
	│
    ├── venv                            <- folder with virtual environment
	│
    ├── app.py                          <- app for running flask	│
	│
    ├── LICENSE                         <- MIT license.
	│
    ├── Procfile                        <- file for flask
	│
    ├── README.md                       <- the top-level README for developers using this project.
	│
    └── requirements.txt                <- requirements for the project

------------
