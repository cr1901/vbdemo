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
		#for str_pixel in self.iterate_str_pixels(transformed_data):
			#entry_no = palette.index_lookup(pt.PaletteEntry(str_pixel))
			#entry_no = palette.index_lookup(struct.unpack('3B', str_pixel))
			#indexed_data.append(entry_no)
			#entry = palette.str2entry(str_pixel)
			#indexed_data.append(palette.
		#extracted_palette = Palette(transformed_data, init_palette_dict, True)
		
		#indexed_data = []
		#for entry in extracted_palette.next_entry(transformed_data, 3):
		#	entry = entry[::-1]
		#	indexed_data.append(extracted_palette.rgb_index[entry])
		
		#return None
		return pt.PaletteImage(indexed_data, palette, self.width, self.height)
		
	def iterate_str_pixels(self, data):
		for pos in range(0, len(data), 3):
			yield data[pos:pos + 3]
		
			
#def extract_data(f_str, pallete_dict = dict()):
	#second_header_size = struct.unpack('<L', f_str[14:18])	
	#bpp = struct.unpack('<H', f_str[28:30])
	
	#print padding
	#print width
	#print height
	#Extract the red BGR indices only.
	#red_data = data_str[2::3]
	#
	#transformed_data = ''
	#
	##Flip the image vertical wise
	#for h in reversed(range(height)):
	#	start_pixel = h * (width + padding)
	#	end_pixel = start_pixel + width
	#	transformed_data =  transformed_data + red_data[start_pixel:end_pixel]
	
	#print struct.unpack('>86016B', transformed_data)
	#Convert the R values to an index to a pallete
	#red2pal = string.maketrans('\x00\x80\xC0\xFF', '\x00\x01\x02\x03')	
	#indexed_data = transformed_data.translate(red2pal)
	
	#print len(indexed_data)
	#print struct.unpack('>86016B', indexed_data)
	
	#bitindex_data = ''
	#index_struct = struct.Struct('8B')
	#string_struct = struct.Struct('>H')
	#i = 0
	#for b in read_n_bytes(indexed_data, 8):
	#	byte_tuple = index_struct.unpack(b)
	#	#print byte_tuple
	#	#print i
	#	#LSB is left, MSB is right for a given byte
	#	packed_byte_lo = (byte_tuple[3] << 6) + (byte_tuple[2] << 4) + \
	#		(byte_tuple[1] << 2) + (byte_tuple[0])
	#	packed_byte_hi = (byte_tuple[7] << 6) + (byte_tuple[6] << 4) + \
	#		(byte_tuple[5] << 2) + (byte_tuple[4])
	#	packed_short = (packed_byte_hi << 8) + packed_byte_lo
	#	bitindex_data = bitindex_data + string_struct.pack(packed_short)
	#	i = i + 1
		
	#tile_data = ''
	#width_in_chars = width/8
	#height_in_chars = height/8
	#bytes_per_tile_row = 2
	#
	#pad_width = (round512(width)/8 - width_in_chars)
	#pad_height = (round512(height)/8 - height_in_chars) * (width_in_chars + pad_width)
	#for h_char in range(0,height_in_chars):
	#	for w_char in range(0,width_in_chars):
	#		for tile_row in range(8):
	#			start_index = bytes_per_tile_row*width_in_chars*(8*h_char + tile_row) + bytes_per_tile_row*w_char
	#			tile_data = tile_data + bitindex_data[start_index] 
	#			tile_data = tile_data + bitindex_data[start_index + 1]
	#			print (start_index, h_char, w_char, tile_row)
	#	#Bytes per row * rows per tile * extra tiles required to multiple of 512 		
	#	tile_data = tile_data + '\0'*2*8*pad_width
	#tile_data = tile_data + '\0'*2*8*pad_height
        #
	##return bitindex_data
	#return tile_data
	#return indexed_data
	
#def read_n_bytes(data, n_bytes):
#	for pos in xrange(0, len(data), n_bytes):
#		yield data[pos:pos + n_bytes]
