Bike paths visualiser   
========

### A Visualisation of the journeys taken by Dublin Bikes users.

The code takes station population data, scraped from the [Dublin bikes site](http://www.dublinbikes.ie/), to create a series possible journeys. By examining how the station populations change with time we can see when bikes leave and arrive at stations. Journeys are estimated by matching a beginning, a start time and station number, with an end, an arrival time and station number. Path data is approximated from [Google maps](www.maps.google.com). 

Individual frames are rendered using the [matplotlib](http://matplotlib.org/) library, these are then compiled into a video using _ffmpeg_.

