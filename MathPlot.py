import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline # Juputer magic to display plots in the notebook

x = np.linspace(start=0,stop=20,num=50)

# plot y = 12-x 
y = 12-x 
plt.plot(x, y, 'b', label='y=12-x')

# plot y = 34.5/x
y2 = 34.5/x
plt.plot(x, y2, 'r-', label=r'$y=\frac{34.5}{x}$')

# Add features to our finger
plt.legend()
plt.grid(True, linestyle=':')
plt.xlim([0,12])
plt.ylim([0,13])
plt.title('Math Homework Q12')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
plt.savefig("MathPlot.png")


"""
Line Properties
===============
A line appearing in a plot has several properties including color, transparency, style, width and markers. 
We can set these properties when we call plt.plot using the following keyword arguments:
alpha:      	            transparency (0.0 transparent through 1.0 opaque)
color (or c):       	    any matplotlib color
label:                 	    text appearing in legend
linestyle (or ls):     	    solid, dashed, dashdot, dotted
linewidth (or lw):  	    set width of the line
marker:                	    set marker style
markeredgecolor (or mec):	any matplotlib color
markerfacecolor (or mfc):	any matplotlib color
markersize (or ms):     	size of the marker

Colors
========
b	blue
g	green
r	red
c	cyan
m	magenta
y	yellow
k	black
w	white

Markers
===========
.	point
o	circle
v	triangle down
^	triangle up
s	square
p	pentagon
*	star
+	plus
x	x
D	diamond

Line Styles
=============
-	solid line style
--	dashed line style
-.	dash-dot line style
:	dotted line style

Pyplot Functions
===================
plt.xlim:       set x limits
plt.ylim:   	set y limits
plt.grid:    	add grid lines
plt.title:  	add a title
plt.xlabel: 	add label to the horizontal axis
plt.ylabel: 	add label to the vertical axis
plt.axis:   	set axis properties (equal, off, scaled, etc.)
plt.xticks:    	set tick locations on the horizontal axis
plt.yticks: 	set tick locations on the vertical axis
plt.legend: 	display legend for several lines in the same figure
plt.savefig:   	save figure (as .png, .pdf, etc.) to working directory
plt.figure: 	create a new figure and set its properties
"""