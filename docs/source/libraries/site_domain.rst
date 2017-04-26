Site 
====

The ``site`` library contains functionality to make a django project
globally aware of the site that is being processed in the current 
request.

Right now, sites are identified by interrogating the Host header sent in a 
request e.g. a Host ``www.eurogamer.net`` is for the site ``eurogamer.net`` .  
It's possible that in future, we could alternatively identify the
current site by inspecting the requested URL e.g. ``auth.gamer-network.net/eurogamer/...``

Using the site library 
----------------------

A word on thread local storage
------------------------------

Reference
---------

