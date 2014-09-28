import bmpreader
import carray
import struct

class VBTileException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return self.msg

class VBImageException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return self.msg
		
class VBPaletteException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return self.msg

class VBSceneException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return self.msg

#Coordinates are represented in characters.
class VBTile:
	def __init__(self, IndexData, Xpos, Ypos, XMax, YMax):
		self.data = []
		self.bytes_per_tile_row = 2
		for v_offset in range(8):
			start_index = self.bytes_per_tile_row*XMax*(8*Ypos + v_offset) + self.bytes_per_tile_row*Xpos
			self.data = self.data + IndexData[start_index:start_index + 8]
			
	def __str__(self):
		print_str = ''
		for v_offset in range(8):
			start_index = v_offset*8
			stop_index = start_index + 8
			print_str = print_str + 'Row ' + v_offset + ': ' + \
				self.data[start_index:stop_index] + '\n'
		return print_str
		#for
		
class NullVBTile(VBTile):
	def __init__(self):
		self.data = [0]*16
		
	
	
class VBPalette:
	def __init__(self, palette):
		#self.index = [dict()]
		#self.value = [[]]
		#self.num_palettes = 0
		self.index = dict()
		self.value = []
		
		print palette.rgb_value
		for entry_no, r_val in enumerate(palette.rgb_value):
			self.index[r_val[0]] = entry_no
			self.value.append(r_val[0])

	#def.append(
		
	def __str__(self):
		print_str = ''
		for index, entry in enumerate(self.value):
			print len(entry)
			print_str = print_str + str(index) + ': ' + str(struct.unpack('B', entry)) + ', '
		return print_str
			
	#def add_entries(self, vb_palette_table):
	#	pass
	
	#VB images can have one of eight palettes per character. If more than
	#4 colors exist in the entire image, split the palettes across
	#4 color boundaries.
		
	
	
class VBIndex:
	def __init__(TileIndex, FlipX = False, FlipY = False):
		pass


class VBImage:
	def __init__(self, palette_image):
		self.width = palette_image.width
		self.height = palette_image.height
		self.width_in_chars = self.width/8
		self.height_in_chars = self.height/8
		self.pad_width = (self.round512(self.width)/8 - self.width_in_chars)
		self.pad_height = (self.round512(self.height)/8 - self.height_in_chars) #* \
			#(self.width_in_chars + self.pad_width)
			
		check_legal_dimensions()
		self.tile_list = []
		for h_char in range(0,height_in_chars):
			for w_char in range(0,width_in_chars):
				tile_list.append(VBTile(palette_image.palette_indices, w_char, h_char, \
					self.width_in_chars, self.height_in_chars))
		#Bytes per row * rows per tile * extra tiles required to multiple of 512

			for pad_w in range(pad_width):
				tile_list.append(NullVBTile)
			tile_data = tile_data + '\0'*2*8*pad_width
		tile_data = tile_data + '\0'*2*8*(self.pad_height)*(self.width_in_chars + self.pad_width)
		
		
		
			
	def round512(number):
		return (number - (number % 512)) + 512
		
	def check_legal_dimensions():
		if (self.height % 8) != 0 or (self.width % 8) != 0:
			raise VBImageException
	
class VBScene:
	def __init__(self, MasterPalette, TileImageArray = None):
		self.char_table = []
		self.reverse_char_lookup = dict()
		self.index_table = []
		self.palette_table = []
		self.image_table = []
		self.num_chars = 0
		self.num_bgs = 0
		self.bg_size = 0
		
		#self.palette_table.append(
		self.num_palettes = 1
		
		
		
		if TileImageArray:
			for tileimg in TileImageArray:
				self.add_image(tileimg)
	
	def add_image(self, TileImage):
		
		
		for tile in TileImage.tile_list:
			self.check_valid_palette(tile, TileImage.palette)
			#Check that palette is valid
			
			#if self.reverse_char_lookup.get(tile) is None:
			#print struct.unpack('<8H', tile)
				
				#char_dict[tile] = struct.pack('>H', num_chars)
				#num_chars = num_chars + 1
	
	#def raw_char
	
	def check_valid_palette(self, tile, palette_list):
		tile_palette = set(tile.data) #Extract the unique palette indices for the tile.
		if len(tile_palette) > 4:
			raise VBSceneException('Invalid palette detected!')
		print tile_palette
	
	#def write_char_file(self, Filename, ArrayName):
	#	carray_writer = carray.ArrayWriter()
	#	pass
	
	#def write_bg_files(self, Filenames, ArrayNames):
	#	pass
	
	#This will most likely be altered to account for various legal
	#BG allocations (i.e. BGs which take 4 segments must be on a boundary of 4)
	#but for now assume input is okay.
	def check_limits(num_chars_to_add, new_bg_size):
		if (self.num_chars + num_chars_to_add) > 2048:
			raise VBSceneException('Number of characters which can' + \
				'be stored has been exhausted!')
			
		if (self.bg_size + new_bg_size) > (8*1024*14):
			raise VBSceneException('BG memory has been exhausted!')	
		
