# VortexBaseanator
Pre-Alpha Tool for helping visualize and understand vortex math in different base number systems.

Command Line Interface.

[number to print] [base] [start blue line at] [ add to blue line every iteration ]


example;
	
	python main.py 30 10 3 6
	
Which means; print 30 iterations of base 10, set the blue line's starting position to 3, and increment by 6 every iteration.
	
Currently ALL field are required but I am working on addressing that issue.
	
After iterating over a base check the "images" folder for an image containing a visual representation of the base you just iterated over. 
Make sure you run through enough iterations to loop through the base at least once or the visualization may not be accurate. I would say, to be safe, iterate for 3x your base.

You may delete the included images in the "images" folder, they are included for demonstration purposes only.
