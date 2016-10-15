## QR project
Haitem Ben Yahia & Bram van den Akker

### Execute project
##### Using bash

Executing `run.sh` sets up a http webserver and runs the graph generator. It should open localhost:8000 to display the output graph.

> sh run.sh

##### Webserver and generator seperately
First run setup a python webserver inside the project folder (Where index.html is located). 
> python -m SimpleHTTPServer

Than run the script. The webserver doesn't need to be restarted each time the scripts is ran.
> python main.py

#### Run example
In case you only want to see the example output (after running the full program). 

Start the python webserver.
> python -m SimpleHTTPServer

Point your browser to the webserver location.
> http://localhost:8000/
