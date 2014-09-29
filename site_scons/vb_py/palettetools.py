import struct

#A large number of these classes exist solely for:
#1. Ease of following the code
#2. Creating hash tables using classes as the key (for reverse table lookup).
class PaletteEntry:
	def __init__(self, R=0, G=0, B=0):
		self.r = R
		self.g = G
		self.b = B
		
	def __init__(self, RawString):
		(self.r, self.g, self.b) = struct.unpack('3B', RawString)
	
	#Not really correct (what about palettes with alpha?), but will do for now.	
	def __eq__(self, another):
		if hasattr(another, 'r') and hasattr(another, 'g') and hasattr(another, 'b'):
			if (self.r, self.g, self.b) == (another.r, another.g, another.b):
				return True
		return False
		
	def __hash__(self):
		return hash((self.r, self.g, self.b))
		
	def __str__(self):
		return str((self.r, self.g, self.b))
		
	def __len__(self):
		return 3
		
		
#Limitations: No alpha channel
#Palette entries must be unique (mainly due to using a dictionary).
class PaletteTable:
	def __init__(self, RawString):
		self.entry_table = []
		self.index = dict()
		self.num_entries = 0
		
		#Future enhancement- specify existing entries via dict?
		"""if InitialDict is not None:
			self.rgb_index = InitialDict
			self.rgb_value = sorted(self.rgb_index.iterkeys(), key=lambda k: self.rgb_index[k])
			self.num_entries = len(InitialDict)
		else:
			self.rgb_index = dict()
			self.rgb_value = []
			self.num_entries = 0"""
		
		for pal_string in self.next_entry(RawString, 3):
			#if len(palette_entry) != 3:
			#	raise ValueError
			palette_entry = PaletteEntry(pal_string)
			
			
			#if self.rgb_index.get(palette_entry) is None:
			self.index[palette_entry] = self.num_entries
			self.entry_table.append(palette_entry)
			self.num_entries = self.num_entries + 1
		
		
		if isinstance(PaletteTable, dict):
			pass
			
				
	def __str__(self):
		print_str = ''
		for index, entry in enumerate(self.entry_table):
			print_str = print_str + str(index) + ': ' + str(entry) + ', '
		return print_str
	
	def next_entry(self, data, n_bytes):
		for pos in xrange(0, len(data), n_bytes):
			yield data[pos:pos + n_bytes]
			
	def str2entry(self, RawString):
		return PaletteEntry(RawString)
			
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
		
	def __eq__(self, another):
		return hasattr(another, 'data') and self.data == another.data
		
	def __hash__(self):
		return hash(self.data)
		
	def __str__(self):
		print_str = ''
		for v_offset in range(8):
			start_index = v_offset*8
			stop_index = start_index + 8
			print_str = print_str + 'Row ' + str(v_offset) + ': ' + \
				str(self.data[start_index:stop_index]) + '\n'
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