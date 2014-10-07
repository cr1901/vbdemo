import struct
import string
import math

import palettetools as pt

class BMPException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return self.msg
		
class Bitmap:
	def __init__(self, Filename):
		self.filename = Filename
		with open(self.filename, 'rb') as fp:
			self.raw_string = fp.read()		
		self.check_if_BMP()
		self.width = struct.unpack('<L', self.raw_string[18:22])[0]
		self.height = struct.unpack('<L', self.raw_string[22:26])[0]
		self.padding = self.width % 4
		self.data_offset = struct.unpack('<L', self.raw_string[10:14])[0]
		self.data_string = self.raw_string[self.data_offset:]
		
	def check_if_BMP(self):
		if self.raw_string[0:2] != 'BM':
			raise BMPException('File does not appear to be a bitmap!')
		elif struct.unpack('<H', self.raw_string[28:30])[0] != 24:
			raise BMPException('Bitmap is incorrect bit depth (expected 24)!')
			
	#A set of initial palette entries needs to be passed in to the bmp conversion
	#The entries SHOULD be the same as the entries input to other later functions,
	#but this is not required. Just keep in mind that if the required input
	#palettes don't match between stages, they will be treated as two seperate
	#palettes that can be chosen.
	def to_palette_image(self, palette):
		indexed_data = []
		row_data = ''
		row_reversed_data = ''
		tuple_struct = struct.Struct('3B')
		
		#Flip the BMP so rows are in order.
		for h in reversed(range(self.height)):
			start_pixel = h * (self.width + self.padding) * 3
			end_pixel = start_pixel + self.width*3
			#row_reversed_data = row_reversed_data + self.data_string[start_pixel:end_pixel]
			row_len = len(self.data_string[start_pixel:end_pixel])
			#transformed_data = ''.join((i for j in zip(r_channel, g_channel, b_channel) for i in j))
		
		
			#for str_pixel in self.iterate_str_pixels(row_data):
			for pos in range(0, row_len, 3):
				#pass
				str_pixel = self.data_string[start_pixel+pos:start_pixel+pos+3]
				#entry = 0
				#Faster than creating a palette entry each time, and using
				#that hash. The hash fcn is mainly provided for conveniene.
				entry = palette.index[tuple_struct.unpack(str_pixel[::-1])]
				indexed_data.append(entry)
				
		return pt.PaletteImage(indexed_data, palette, self.width, self.height)
		
	def iterate_str_pixels(self, data):
		for pos in range(0, len(data), 3):
			yield data[pos:pos + 3]
			
