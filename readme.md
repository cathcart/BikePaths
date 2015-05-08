Bike paths visualiser   
========

### A Visualisation of the journies taken by Dublin Bikes users.

The code takes station population data, scraped from [dublin bikes](http://www.dublinbikes.ie/), to create a series possible journies. 

Path data is taken from [Google maps](www.maps.google.com). 

Individual frames are rendered using the [matplotlib](http://matplotlib.org/) library, these are then compiled using _ffmpeg_.

The visualisations are for

run with mencoder mf://alt_*.png -mf fps=24:type=png -ovc lavc -lavcopts vcodec=mpeg4:mbd=0:trell -oac copy -o output.avi


