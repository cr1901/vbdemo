import struct
import string
import math

class BMPException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return self.msg
		
class TileImageException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return self.img

class PaletteEntry:
	def __init__(self, R=0, G=0, B=0):
		self.r = R
		self.g = G
		self.b = B
		
	def __init__(self, RawString):
		pass
		
		
	#def __eq__

#Limitations: No alpha channel
#Palette entries must be unique (mainly due to using a dictionary).
class Palette:
	def __init__(self, RawString, InitialDict = None, swap_raw_order=False):
		if InitialDict is not None:
			self.rgb_index = InitialDict
			self.rgb_value = sorted(self.rgb_index.iterkeys(), key=lambda k: self.rgb_index[k])
			self.num_entries = len(InitialDict)
		else:
			self.rgb_index = dict()
			self.rgb_value = []
			self.num_entries = 0
			
			
		#struct.Struct('>3B'
		
		for palette_entry in self.next_entry(RawString, 3):
			if len(palette_entry) != 3:
				raise ValueError
			
			#Palette expects RGB... Bitmap outputs BGR
			if swap_raw_order:
				palette_entry = palette_entry[::-1]
				
			#palette_tuple = 
				
			if self.rgb_index.get(palette_entry) is None:
				self.rgb_index[palette_entry] = self.num_entries
				self.rgb_value.append(palette_entry)
				self.num_entries = self.num_entries + 1
				
	def __str__(self):
		print_str = ''
		for index, entry in enumerate(self.rgb_value):
			print_str = print_str + str(index) + ': ' + str(struct.unpack('>3B', entry)) + ', '
		return print_str
	
	def next_entry(self, data, n_bytes):
		for pos in xrange(0, len(data), n_bytes):
			yield data[pos:pos + n_bytes]
			
class Tile:
	def __init__(self, IndexData, XSize, YSize, Xpos, Ypos, RowWidth):
		self.data = []
		self.x_size = XSize
		self.y_size = YSize
		self.x_pos = Xpos
		self.y_pos = Ypos
		for v_offset in range(self.y_size):
			start_index = RowWidth*(self.y_size*self.y_pos + v_offset) + \
				self.x_size*self.x_pos
			stop_index = start_index + self.x_size
			#print (start_index, stop_index)
			self.data = self.data + IndexData[start_index:stop_index]
		#print self.data
			
	def __str__(self):
		print_str = ''
		for v_offset in range(8):
			start_index = v_offset*8
			stop_index = start_index + 8
			print_str = print_str + 'Row ' + str(v_offset) + ': ' + \
				str(self.data[start_index:stop_index]) + '\n'
		return print_str
		
	def generate_key(self):
		return ''.join(map(str, self.data))
		
		
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
			
	def to_palette(self, init_palette_dict = None):
		transformed_data = ''
		
		#Flip the BMP so rows are in order.
		for h in reversed(range(self.height)):
			start_pixel = h * (self.width + self.padding) * 3
			end_pixel = start_pixel + self.width*3
			transformed_data =  transformed_data + self.data_string[start_pixel:end_pixel]
			
		extracted_palette = Palette(transformed_data, init_palette_dict, True)
		
		indexed_data = []
		for entry in extracted_palette.next_entry(transformed_data, 3):
			entry = entry[::-1]
			indexed_data.append(extracted_palette.rgb_index[entry])
		
		return PaletteImage(indexed_data, extracted_palette, self.width, self.height)
		
		
			
class PaletteImage:
	def __init__(self, Index, Palette, Width, Height):
		self.palette_indices = Index
		self.palette = Palette
		self.width = Width
		self.height = Height
		
	def __str__(self):
		print_str = 'Palette: ' + str(self.palette) + '\nIndices:\n'
		for h in range(self.height):
			start_index = h*self.width
			stop_index = start_index + self.width
			print_str = print_str + 'Row ' + str(h) + \
				': ' + str(self.palette_indices[start_index:stop_index]) + '\n'
		return print_str
		
		
class TileImage:
	def __init__(self, palette_image, TileX, TileY):
		self.width = palette_image.width
		self.height = palette_image.height
		self.palette = palette_image.palette
		self.tile_xdim = TileX
		self.tile_ydim = TileY
		self.check_legal_dimensions()
		
		self.width_in_chars = self.width/self.tile_xdim
		self.height_in_chars = self.height/self.tile_ydim
		#self.pad_width = (self.round512(self.width)/8 - self.width_in_chars)
		#self.pad_height = (self.round512(self.height)/8 - self.height_in_chars) #* \
			#(self.width_in_chars + self.pad_width)
			
		self.tile_list = []
		for h_char in range(0,self.height_in_chars):
			for w_char in range(0,self.width_in_chars):
				#print (w_char, h_char)
				self.tile_list.append(Tile(palette_image.palette_indices, self.tile_xdim, \
					self.tile_ydim, w_char, h_char, self.width))
		#Bytes per row * rows per tile * extra tiles required to multiple of 512

			#for pad_w in range(pad_width):
			#	tile_list.append(NullVBTile)
			#tile_data = tile_data + '\0'*2*8*pad_width
		#tile_data = tile_data + '\0'*2*8*(self.pad_height)*(self.width_in_chars + self.pad_width)
		
	def __str__(self):
		#Try to print the tiles as if were rendered for real.
		#print len(self.tile_list)
		print_str=''
		for h_char in range(0,self.height_in_chars):
			start_tile = h_char*self.width_in_chars
			#print start_tile
			for j in range(0, self.tile_ydim):
				start_tile = h_char*self.width_in_chars
				start_offset = j*self.tile_xdim
				end_offset = start_offset + self.tile_xdim
				for i in range(0, self.width_in_chars):
					#if j == 0:
					#	print_str = print_str + 'Tile (' + \
					#		str(i) + ', ' + str(h_char) + '): '
					print_str = print_str + \
						str(self.tile_list[start_tile + i].data[start_offset:end_offset]) + ' '
				print_str = print_str + '\n'
			print_str = print_str + '\n'			
		return print_str

	def check_legal_dimensions(self):
		if (self.height % self.tile_ydim) != 0 or (self.width % self.tile_xdim) != 0:
			raise VBImageException('Image dimensions are not a multiple of the tile dimensions!')
		
		
			
def extract_data(f_str, pallete_dict = dict()):
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
	
	bitindex_data = ''
	index_struct = struct.Struct('8B')
	string_struct = struct.Struct('>H')
	i = 0
	for b in read_n_bytes(indexed_data, 8):
		byte_tuple = index_struct.unpack(b)
		#print byte_tuple
		#print i
		#LSB is left, MSB is right for a given byte
		packed_byte_lo = (byte_tuple[3] << 6) + (byte_tuple[2] << 4) + \
			(byte_tuple[1] << 2) + (byte_tuple[0])
		packed_byte_hi = (byte_tuple[7] << 6) + (byte_tuple[6] << 4) + \
			(byte_tuple[5] << 2) + (byte_tuple[4])
		packed_short = (packed_byte_hi << 8) + packed_byte_lo
		bitindex_data = bitindex_data + string_struct.pack(packed_short)
		i = i + 1
		
	tile_data = ''
	width_in_chars = width/8
	height_in_chars = height/8
	bytes_per_tile_row = 2
	
	pad_width = (round512(width)/8 - width_in_chars)
	pad_height = (round512(height)/8 - height_in_chars) * (width_in_chars + pad_width)
	for h_char in range(0,height_in_chars):
		for w_char in range(0,width_in_chars):
			for tile_row in range(8):
				start_index = bytes_per_tile_row*width_in_chars*(8*h_char + tile_row) + bytes_per_tile_row*w_char
				tile_data = tile_data + bitindex_data[start_index] 
				tile_data = tile_data + bitindex_data[start_index + 1]
				print (start_index, h_char, w_char, tile_row)
		#Bytes per row * rows per tile * extra tiles required to multiple of 512 		
		tile_data = tile_data + '\0'*2*8*pad_width
	tile_data = tile_data + '\0'*2*8*pad_height

	#return bitindex_data
	return tile_data
	#return indexed_data
	
#def read_n_bytes(data, n_bytes):
#	for pos in xrange(0, len(data), n_bytes):
#		yield data[pos:pos + n_bytes]
