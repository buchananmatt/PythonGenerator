#	Matthew Buchanan
#	20 September 2017
#	manualslice.py
#
#	1) input a tool path from a gcode file
#	2) input number of layers and desired constant stickout
#	3) create a g-code file that does not need modification
import sys
import os.path

toolpath_filestring = "./toolpath.gcode"
toolpath_file = open(toolpath_filestring, "r")
toolpath = toolpath_file.read()

first_line = toolpath.split('\n', 1)[0]
tokens = first_line.split(' ')

num_layers = int(sys.argv[1])
stickout = int(sys.argv[2])
feed_rate = sys.argv[3]
x_start = tokens[1]
y_start = tokens[2]

layer_count = 0
layer_height = 2

for i in range(0,200):
			filestr = './output{}.gcode'.format(i)
			if os.path.isfile(filestr):
				print "file exists"
				continue
			else:
				file = open(filestr, "w+")
				break

start_file = (	"G21\n"
				"G90\n"
				"G28\n")

def before_toolpath(stickout, layer_height, layer_count, x_start, y_start, feed_rate):
	return ("G0 Z{}\n"
			"G0 F4000 {} {}\n"
			"M770\n"
			"G4 S1\n"
			"M710\n"
			"G4 P100\n"
			"M750 S10000\n"
			"G1 F{}\n"
			"M701\n" ).format((stickout+(layer_height*layer_count)), x_start, y_start, feed_rate)

#before_toolpath = (	"G0 Z{}\n"
#					"G0 F4000 X{} Y{}\n"
#					"M770\n"
#					"G4 S1\n"
#					"M710\n"
#					"G4 P100\n"
#					"M750 S10000\n"
#					"G1 F{}\n"
#					"M701\n" ).format((stickout+(layer_height*layer_count)), x_start, y_start, feed_rate)

after_toolpath = (	"\nM400\n"
					"M702\n"
					"M760\n"
					"G4 P300\n"
					"M720\n"
					"M780\n")

end_file = (	"G0 X75 Y100 Z20\n"
				"M84\n")

print start_file 
with open(filestr, "a+") as file:
			file.write(start_file)

for x in range(0, num_layers):
	print before_toolpath(stickout, layer_height, layer_count, x_start, y_start, feed_rate)
	print toolpath 
	print after_toolpath 

	with open(filestr, "a+") as file:
			file.write(before_toolpath(stickout, layer_height, layer_count, x_start, y_start, feed_rate))
			file.write(toolpath)
			file.write(after_toolpath)

	layer_count = layer_count + 1;
print end_file
with open(filestr, "a+") as file:
			file.write(end_file)
