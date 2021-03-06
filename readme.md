Dublin Bikes journey visualiser   
========

### A Visualisation of the journeys taken by Dublin Bikes users.

BikePaths takes station population data, scraped from the [Dublin Bikes site](http://www.dublinbikes.ie/), to create a series of possible journeys. By examining how the station populations change with time we can see when bikes leave and arrive at stations. Journeys are estimated by matching a beginning, a start time and station number, with an end, an arrival time and station number. Path data is approximated from [Google maps](www.maps.google.com). 

Individual frames are rendered using the [matplotlib](http://matplotlib.org/) library, these are then compiled into a video using _ffmpeg_.

This work was featured in the [Science Gallery Hack the City](https://dublin.sciencegallery.com/hackthecity/) exhibit as part of the [DynamicDublin](https://dublin.sciencegallery.com/hackthecity/dynamicdublin/) group.


### Visualisations
https://www.youtube.com/watch?v=_9m9Ygdxp8Q&index=1&list=PLYHnaycp11CSIvhWhJAhdekKJINDZN0ez

[![BikePaths visualised journies](http://img.youtube.com/vi/_9m9Ygdxp8Q/0.jpg)](https://www.youtube.com/watch?v=_9m9Ygdxp8Q&index=1&list=PLYHnaycp11CSIvhWhJAhdekKJINDZN0ez)
