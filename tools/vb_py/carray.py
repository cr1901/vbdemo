import struct

#Todo- Add header/table generator that is an Observer for the current array writer
#to keep track of table entries and array names written out by the array writer.

class ArrayWriter:
	structformat = {'char' : 'B', 'signed char' : 'B', 'unsigned char' : 'B', \
		'short' : 'H', 'signed short' : 'H', 'unsigned short' : 'H', \
		'int' : 'I', 'signed int' : 'I', 'unsigned int' : 'I', \
		'long' : 'L', 'signed long' : 'L', 'unsigned long' : 'L'}
		
	typesize = {'char' : 1, 'signed char' : 1, 'unsigned char' : 1, \
		'short' : 2, 'signed short' : 2, 'unsigned short' : 2, \
		'int' : 2, 'signed int' : 2, 'unsigned int' : 2, \
		'long' : 4, 'signed long' : 4, 'unsigned long' : 4}
	
	def __init__(self, ArrayType = 'short', ElementsPerLine = 8, PadVal = 0, \
		OffsetComments=False, StartOffset=0, OffsetInc=1, Header = None):
		self.arraytype = ArrayType
		self.elements_per_line = ElementsPerLine
		self.pad_val = PadVal
		self.offset_comments = OffsetComments
		self.start_offset = StartOffset
		self.offset_inc = OffsetInc
		if not Header:
			self.header = "/*** Generated using the carray.py tool. ***/\n\n"
		else:
			self.header = Header
	
	def write_file(self, outname, data, arrayname, pad_to=None):
		outstr = ''
		outstr = outstr + self.write_header()
		outstr = outstr + self.write_string(data, arrayname, pad_to)
		outfp = open(outname, 'wb')
		outfp.write(outstr)
		outfp.close()
	
	def write_string(self, data, arrayname, pad_to=None):
		array_str = "const " + self.arraytype + " " + arrayname + "[] = { \n" #'\\\n' ?
						
		if pad_to:
			#print 'padding'
			pad_bytes = chr(self.pad_val) * ((pad_to * ArrayWriter.typesize[self.arraytype]) - len(data))
			data = data + pad_bytes
			#print len(data)
		
		elements_remainder = (len(data) / ArrayWriter.typesize[self.arraytype]) % self.elements_per_line
		bytes_per_line = self.elements_per_line * ArrayWriter.typesize[self.arraytype]
		format_specifier = '{0:#0' + str((ArrayWriter.typesize[self.arraytype] * 2) + 2) + 'X},'
		
		if self.offset_comments:
			comment_str = '/* {0:#X} */'
		else:
			comment_str = ''
			
		curr_offset = self.start_offset
		
		if isinstance(data, str):
			struct_writer = struct.Struct('>' + str(self.elements_per_line) + ArrayWriter.structformat[self.arraytype])
			for bytes in self.read_n_bytes(data, self.elements_per_line * ArrayWriter.typesize[self.arraytype]):
			#http://stackoverflow.com/questions/4440516/in-python-is-there-an-elegant-way-to-print-a-list-in-a-custom-format-without-ex
				try:
					curr_line = '\t' + ''.join(format_specifier.format(k) \
						for k in struct_writer.unpack(bytes)) + '\t' + \
						comment_str.format(curr_offset) + '\n' #'\\\n' ?
					curr_offset = curr_offset + self.offset_inc
				except:
					last_data = struct.unpack('>' + str(elements_remainder) + \
						ArrayWriter.structformat[self.arraytype], bytes)
					curr_line = '\t' + ''.join(format_specifier.format(k) \
						for k in last_data) + '\t' + \
						comment_str.format(curr_offset) + '\n' #'\\\n' ?
				array_str = array_str + curr_line
		else:
			pass
			#Not really working properly for now...
			#for bytes in self.read_n_bytes(data, self.elements_per_line * ArrayWriter.typesize[self.arraytype]):
			#	curr_line = ''.join(format_specifier.format(k) \
			#		for k in bytes) + '\n' #'\\\n' ?
			#	outfp.write(curr_line)
		last_comma = array_str.rfind(',') #Remove the last comma from end of array.
		array_str = array_str[:last_comma] + ' '  + array_str[last_comma + 1:] + " };\n\n"
		return array_str #Why is last newline removed?
		
	def write_header(self):
		return self.header
		
	#http://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
	def read_n_bytes(self, data, n_bytes):
		for pos in range(0, len(data), n_bytes):
			yield data[pos:pos + n_bytes]
