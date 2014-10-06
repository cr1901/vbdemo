import struct

class ArrayWriter:
	structformat = {'char' : 'B', 'signed char' : 'B', 'unsigned char' : 'B', \
		'short' : 'H', 'signed short' : 'H', 'unsigned short' : 'H', \
		'int' : 'I', 'signed int' : 'I', 'unsigned int' : 'I', \
		'long' : 'L', 'signed long' : 'L', 'unsigned long' : 'L'}
		
	typesize = {'char' : 1, 'signed char' : 1, 'unsigned char' : 1, \
		'short' : 2, 'signed short' : 2, 'unsigned short' : 2, \
		'int' : 2, 'signed int' : 2, 'unsigned int' : 2, \
		'long' : 4, 'signed long' : 4, 'unsigned long' : 4}
	
	def __init__(self):
		pass
		
	
	def write(self, outname, data, arrayname, arraytype, elements_per_line, pad_to=None, pad_val=0):
		outfp = open(outname, 'wb')
		outfp.write("/*** Generated using the carray.py tool. ***/\n")
		outfp.write("\n")
		outfp.write("const " + arraytype + " " + arrayname + "[] = { \n") #'\\\n' ?
		
		
						
		if pad_to:
			#print 'padding'
			pad_bytes = chr(pad_val) * ((pad_to * ArrayWriter.typesize[arraytype]) - len(data))
			data = data + pad_bytes
			#print len(data)
		
		elements_remainder = (len(data) / ArrayWriter.typesize[arraytype]) % elements_per_line
		bytes_per_line = elements_per_line * ArrayWriter.typesize[arraytype]
		format_specifier = '{0:#0' + str((ArrayWriter.typesize[arraytype] * 2) + 2) + 'x}, '
		
		if isinstance(data, str):
			struct_writer = struct.Struct('>' + str(elements_per_line) + ArrayWriter.structformat[arraytype])
			for bytes in self.read_n_bytes(data, elements_per_line * ArrayWriter.typesize[arraytype]):
			#http://stackoverflow.com/questions/4440516/in-python-is-there-an-elegant-way-to-print-a-list-in-a-custom-format-without-ex
				try:
					curr_line = ''.join(format_specifier.format(k) \
						for k in struct_writer.unpack(bytes)) + '\n' #'\\\n' ?
				except:
					last_data = struct.unpack('>' + str(elements_remainder) + \
						ArrayWriter.structformat[arraytype], bytes)
					curr_line = ''.join(format_specifier.format(k) \
						for k in last_data)
				outfp.write(curr_line)
		else:
			pass
			#Not really working properly for now...
			#for bytes in self.read_n_bytes(data, elements_per_line * ArrayWriter.typesize[arraytype]):
			#	curr_line = ''.join(format_specifier.format(k) \
			#		for k in bytes) + '\n' #'\\\n' ?
			#	outfp.write(curr_line)
		
		outfp.seek(-3, 1) #Go back two spaces and remove the last comma.	
		outfp.write(" \n};\n")
		outfp.close()
		
		
	#http://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
	def read_n_bytes(self, data, n_bytes):
		for pos in xrange(0, len(data), n_bytes):
			yield data[pos:pos + n_bytes]
			
			
"""class TypeDescription:

	
	def __init__(type):
		self.size = Size
		self.format = StructFormat"""
