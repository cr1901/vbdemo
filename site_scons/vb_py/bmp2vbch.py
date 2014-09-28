import optparse
import os.path
import struct

import bmpreader
import vbgfx
import carray




def bmp2vbch_scons(target, source, env):
	pass

def bmp2vbch(bmp_in, charfile = None, compress=True, bgprefix="bg_", charprefix="char_"):
	if charfile is None:
		print "No output character file specified. Array/Output name derive name from {0}".format(args[0])
		outchar_path, outchar_filename_ext = os.path.split(args[0])
		outchar_filename = os.path.splitext(outchar_filename_ext)[0]
		outchar_filename = 'c' + outchar_filename
	else:
		outchar_path, outchar_filename = os.path.split(charfile)
	
	global_palette_dict = {'\x00\x00\x00' : 0, '\x80\x00\x00' : 1, '\xC0\x00\x00' : 2, '\xFF\x00\x00' : 3}
	
	vb_scene = vbgfx.VBScene(global_palette_dict)
	carray_writer = carray.ArrayWriter()
	
	
	#pallete_indices = []
	#char_dict = dict()
	
	bmp_list = []
	palimg_list = []
	tileimg_list = []
	#tilemap = []
	#all_tiles = ''
	
	for bmpfile in bmp_in:
		bmp_list.append(bmpreader.Bitmap(bmpfile))
	
	#Must specify at least the minimum number of colors to fill a single
	#palette table. This data will be preserved verbatim.
	#Other palettes can be omitted/hueristically generated from the "master palette".
	for bmpimg in bmp_list:
		palimg_list.append(bmpimg.to_palette(global_palette_dict))
		
	for palimg in palimg_list:
		tileimg_list.append(bmpreader.TileImage(palimg, 8, 8))
		#print my_tile_image
		
	for tileimg in tileimg_list:
		vb_scene.add_image(tileimg)
	exit()
	
	tile_idx = 0
	char_str = ''
	for tile in bmpreader.read_n_bytes(all_tiles, 16):
		if char_dict.get(tile) is None:
			#print struct.unpack('<8H', tile)
			char_dict[tile] = struct.pack('>H', tile_idx)
			char_str = char_str + tile
			tile_idx = tile_idx + 1
	
	outchar_arrayname = charprefix + outchar_filename
	char_outname = outchar_path + os.path.sep + outchar_filename + ".c"	
	carray_writer.write(char_outname, char_str, outchar_arrayname, 'short', 8)	
	
	for (bgmap, bmpfile) in zip(tilemap, bmp_in):
		bmp_path, bmp_filename_ext = os.path.split(bmpfile)
		bmp_filename = os.path.splitext(bmp_filename_ext)[0]
		bmp_arrayname = bgprefix + bmp_filename
		bmp_outname = bmp_path + os.path.sep + bmp_filename + ".c"
		
		bgindex = ''
		for tile in bmpreader.read_n_bytes(bgmap, 16):
			print struct.unpack('>H', char_dict[tile])
			bgindex = bgindex + char_dict[tile]
			
		carray_writer.write(bmp_outname, bgindex, bmp_arrayname, 'short', 8)
		
		#bmpreader.extract_palettes_and_indices(f_str)
		
		#write_array_short(bmp_outname, bmp_arrayname, f_str)
		
	#print "Creating char array " + charprefix + outchar_filename + " at " + outchar_path + os.path.sep + outchar_filename + ".c"
		
	
def extract_palettes_and_indices(bmp_stream):	
	pass


#http://stackoverflow.com/questions/3753589/packing-and-unpacking-variable-length-array-string-using-the-struct-module-in-py
def unpack_helper(fmt, data):
	size = struct.calcsize(fmt)
	return struct.unpack(fmt, data[:size])
	
	

if __name__ == '__main__':
	parser = optparse.OptionParser(usage="Usage: %prog [options] bmp1 [bmp2 ...]")
	parser.add_option("-b", None, action="store",  type="string", \
		dest="bgprefix", help="Array prefix for background files", default="bg_")
	parser.add_option("-c", None, action="store",  type="string", \
		dest="charprefix", help="Array prefix for character file.", default="char_")
	#Header option?
	parser.add_option("-x", None, action="store_true", dest="compress", \
		 help="Compress character maps and BGs (default: %default)", default=True)
	parser.add_option("-o", None, action="store", type="string", \
		dest="charfile", help="Output character file (default: Name of first bitmap, prefixed with 'c')", default=None)
	(options, args) = parser.parse_args()
	
	if not args:
		print "No input files specified. Aborting."
		exit(-2)
		
	bmp2vbch(args, options.charfile, options.compress, options.bgprefix, options.charprefix)