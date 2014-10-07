import warnings

import bmpreader
import carray
import struct
import palettetools as pt

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
		
class VBBGEntry:
	def __init__(self, PaletteNo = 0, HFlip = False, VFlip = False, CharNo = 0):
		self.palette_no = PaletteNo
		self.hflip = HFlip
		self.vflip = VFlip
		self.char_no = CharNo
		self.str_struct = struct.Struct('>H')
		
	def to_raw(self):
		return (self.palette_no << 14) + (int(self.hflip) << 13) + \
			(int(self.vflip) << 12) + self.char_no

class VBTile(pt.Tile):
	def __init__(self, Data = tuple([0]*64)):
		self.data = Data
		
	def to_raw(self, bytestream=False):
		raw_stream = []
		for row_start in range(0,64,8):
			one_row = self.data[row_start:row_start+8]
			#if bytestream:
			#
			packed_short = packed_byte_lo = (one_row[7] << 14) + (one_row[6] << 12) + \
			(one_row[5] << 10) + (one_row[4] << 8) + \
			(one_row[3] << 6) + (one_row[2] << 4) + \
			(one_row[1] << 2) + (one_row[0])
			raw_stream.append(packed_short)
		return raw_stream	
			
	def flip_raw(self, flip_tuple):
		pass
		
	
	
class VBPaletteTables:
	def __init__(self, paletteTable):
		if paletteTable.num_entries % 4 != 0:
			raise VBPaletteException('Number of unique palette entries specified' + \
				' is not a multiple of 4, and logic to handle such cases' + \
				' is not yet implemented!')
		
		self.entry_table = paletteTable.entry_table
		self.num_used_palettes = paletteTable.num_entries / 4
		if self.num_used_palettes*4 < 32:
			for e in range(self.num_used_palettes*4, 32, 4):
				self.entry_table += self.entry_table[0:4]
		
		#This data determines whether an input tile (pre-transformation)
		#has a correct palette. All the indices within a tile should
		#belong within one set.
		self.palette_sets = [set([s, s + 1, s + 2, s + 3]) for s in range(0,32,4)]
		#for s in range(0,32,4):
		#	self.palette_sets.append(set(self.entry_table[))
		
		#self.palette_sets = set(x) for 
		#self.num_palettes = 0
		#self.index = dict() #Do we need this?
		self.vb_index = [e % 4 for e in range(0,32)]
		self.value = []
		
		#print palette.rgb_value
		#for entry_no, r_val in enumerate(palette.rgb_value):
		#	self.index[r_val[0]] = entry_no
		#	self.value.append(r_val[0])

	#def.append(
		
	def __str__(self):
		print_str = ''
		print_str += self.palette_sets
		for index, entry in enumerate(self.value):
			print len(entry)
			print_str = print_str + str(index) + ': ' + str(struct.unpack('B', entry)) + ', '
		return print_str
	
	def translate_index(self, entries):
		type(entries)
		if isinstance(entries, pt.Tile):
			return VBTile(tuple([e % 4 for e in entries]))
		elif isinstance(entries, list):
			return [e % 4 for e in entries]
		else:
			return entries % 4
	
	def check_valid_palette(self, tile):
		tile_palette = set(tile.data) #Extract the unique palette indices for the tile.
		if len(tile_palette) > 4:
			raise VBPaletteException('Invalid palette detected!')
		#print tile_palette
		
		matched_set_no = 0
		num_matched_sets = 0
		first_matched_set = 0
		for set_no in range(0,8):
			if tile_palette <= self.palette_sets[set_no]:
				#print 'Match: ' + str(set_no)
				#matched_set_no = set_no
				num_matched_sets = num_matched_sets + 1
				if num_matched_sets == 1:
					first_matched_set = set_no
					
		#print num_matched_sets
		if num_matched_sets == 0:
			raise VBPaletteException('Tile''s palette does not match any stored palettes!')
		elif num_matched_sets > 1:
			warnings.warn('Tile''s palette matched more than one stored palette. Using first match.')
		return first_matched_set
		
	#def add_entries(self, vb_palette_table):
	#	pass
	
	#VB images can have one of eight palettes per character. If more than
	#4 colors exist in the entire image, split the palettes across
	#4 color boundaries.
	
class VBCharTable:
	def __init__(self):
		self.char_list = []
		#NoFlip, FlipX, FlipY, FlipXY
		self.reverse_table = (dict(), dict(), dict(), dict())
		self.num_chars = 0
		self.flipxy = ((0, 0), (1, 0), (0, 1), (1, 1))
		
	def reverse_lookup(self, key):
		dict_no = 0
		while dict_no < 1:
			#Only concern ourselves with NoFlip for now...
			try:
				#index_and_flip = self.reverse_table[dict_no][key]
				return (self.reverse_table[0][key], self.flipxy[dict_no])
			except KeyError:
				pass
			dict_no = dict_no + 1
		
		#If we got here, than indeed, the tile does not exist... add it to
		#the dictionaries.
		self.add_tile(key)
		#print 'Curr Tile: ' + str(self.num_chars - 1)
		return (self.num_chars - 1, self.flipxy[0]) #One less because self.num_chars was
		#incremented to next free index.
		
	def add_tile(self, tile):
		self.char_list.append(tile)
		self.reverse_table[0][tile] = self.num_chars
		self.num_chars = self.num_chars + 1
	
#class VBBGSegment:
#	def __init__(self, 

class VBImage:
	def __init__(self, tile_image, palette_tables, char_table):
		self.used_width = tile_image.width
		self.used_height = tile_image.height
		self.full_width = self.round512(tile_image.width)
		self.full_height = self.round512(tile_image.height)
		self.num_segments = (self.full_height/512 * self.full_width/512)
		self.used_width_in_chars = self.used_width/8
		self.used_height_in_chars = self.used_height/8
			
		self.check_legal_dimensions()
		self.entry_list = ()
		
		#Convert the image so that it uses segments
		for seg_y in range(0, self.used_height_in_chars, 64):
			for seg_x in range(0, self.used_width_in_chars, 64):
				used_curr_segy = self.used_height_in_chars - seg_y
				used_curr_segx = self.used_width_in_chars - seg_x				
				#Check if the x/y-direction of the image uses the 
				#entire segment. If so/exceeds the segment,
				#clamp the number of tiles to traverse to
				#the segment length (64).
				if used_curr_segy > 64:
					used_curr_segy = 64
				if used_curr_segx > 64:
					used_curr_segx = 64
					
				for offset_y in range(0, used_curr_segy):
					for offset_x in range(0, used_curr_segx):
						#print seg_x + offset_x, seg_y + offset_y
						curr_tile = tile_image[seg_x + offset_x, seg_y + offset_y]
						pal_no = palette_tables.check_valid_palette(curr_tile)
						curr_vb_tile = palette_tables.translate_index(curr_tile)
						(char_no, flip) = char_table.reverse_lookup(curr_vb_tile)
						#print 'char_no: ' + str(char_no)
						self.entry_list = self.entry_list + tuple([VBBGEntry(pal_no, flip[0], flip[1], char_no)])
						#print curr_tile
					
					for offset_xu in range(used_curr_segx, 64):
						self.entry_list = self.entry_list + tuple([VBBGEntry()])
						#print 'Zero Tile: ' + str((seg_x + offset_xu, seg_y + offset_y))
				
				#If the current row (i.e. traversing across x) is unused, 
				#then the used_curr_segx is irrelevant.
				for offset_yu in range(used_curr_segy, 64):
					for curr_column in range(0,64):
						self.entry_list = self.entry_list + tuple([VBBGEntry()])
						#print 'Zero Tile: ' + str((seg_x + curr_column, seg_y + offset_yu))
		
			
	def round512(self, number):
		return (number - (number % 512)) + 512
		
	def check_legal_dimensions(self):
		if (self.used_height % 8) != 0 or (self.used_width % 8) != 0:
			raise VBImageException('Image dimensions are not a multiple of 8!')
		if self.num_segments not in [1, 2, 4, 8]:
			raise VBImageException('Image cannot be converted to a supported BG segment combination!')
	
class VBScene:
	def __init__(self, MasterPaletteTable, TileImageArray = None):
		self.num_chars = 0
		self.num_bgs = 0
		self.bg_size = 0
		
		#self.palette_table.append(
		self.char_table = VBCharTable()
		self.image_table = []
		self.palette_tables = VBPaletteTables(MasterPaletteTable)
		
		if TileImageArray:
			for tileimg in TileImageArray:
				self.add_image(tileimg)
				
	def __len__(self):
		return self.num_bgs
	
	def add_image(self, TileImage):
		self.image_table.append(VBImage(TileImage, self.palette_tables, self.char_table))
		self.num_bgs = self.num_bgs + 1
		
	def charstr_raw(self):
		char_str = ''
		short_struct = struct.Struct('>8H')
		for char in self.char_table.char_list:
			tile_raw_chars = char.to_raw()
			char_str = char_str + short_struct.pack(*tile_raw_chars)
		return char_str
		
	def bg_raw(self, index):
		bg_str = ''
		short_struct = struct.Struct('>H')
		for entry in self.image_table[index].entry_list:
			entry_raw = entry.to_raw()
			bg_str = bg_str + short_struct.pack(entry_raw)
		return bg_str
		
	#This will most likely be altered to account for various legal
	#BG allocations (i.e. BGs which take 4 segments must be on a boundary of 4)
	#but for now assume input is okay.
	def check_limits(num_chars_to_add, new_bg_size):
		if (self.num_chars + num_chars_to_add) > 2048:
			raise VBSceneException('Number of characters which can' + \
				'be stored has been exhausted!')
			
		if (self.bg_size + new_bg_size) > (8*1024*14):
			raise VBSceneException('BG memory has been exhausted!')	
		
