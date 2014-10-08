import optparse
import os.path
import struct

import bmpreader
import palettetools as pt
import vbgfx
import carray


version = 0.9

def bmp2vbch_cmd(bmp_in, charfile = None, compress=True, bgprefix="bg_", charprefix="char_"):
	if charfile is None:
		print "No output character file specified. Array/Output name derive name from {0}".format(args[0])
		outchar_path, outchar_filename_ext = os.path.split(args[0])
		outchar_filename = os.path.splitext(outchar_filename_ext)[0]
		outchar_filename = 'c' + outchar_filename
	else:
		outchar_path, outchar_filename_ext = os.path.split(charfile)
		outchar_filename = os.path.splitext(outchar_filename_ext)[0]
	#print bmp_in
	#global_palette_dict = ['\x00\x00\x00' : 0, '\x80\x00\x00' : 1, '\xC0\x00\x00' : 2, '\xFF\x00\x00' : 3}
	
	bmp2vbch_header = "\n/* <<<<<<<<<< Generated using the bmp2vbch.py tool, ver" + str(version) + " >>>>>>>>>> */\n\n"
	
	chararray_writer = carray.ArrayWriter(OffsetComments=True, Header = bmp2vbch_header)
	bgarray_writer = carray.ArrayWriter(OffsetComments=True, OffsetInc = 8, Header = bmp2vbch_header)
	global_palette = pt.PaletteTable('\x00\x00\x00\x80\x00\x00\xC0\x00\x00\xFF\x00\x00')
	vb_scene = vbgfx.VBScene(global_palette)
	
	bmp_list = []
	palimg_list = []
	tileimg_list = []
	
	for bmpfile in bmp_in:
		bmp_list.append(bmpreader.Bitmap(bmpfile))
	
	#Must specify at least the minimum number of colors to fill a single
	#palette table. This data will be preserved verbatim.
	#Other palettes can be omitted/hueristically generated from the "master palette".
	
	for bmpimg in bmp_list:
		palimg_list.append(bmpimg.to_palette_image(global_palette))
		
	for palimg in palimg_list:
		tileimg_list.append(pt.TileImage(palimg, 8, 8))
		
	#This section determines whether the supplied bitmaps and extracted chars
	#meet conditions by the hardware. It also modifies the images in any
	#manner deemend necessary.
	for tileimg in tileimg_list:
		vb_scene.add_image(tileimg)
	
	#tile_idx = 0
	char_str = vb_scene.charstr_raw()
	"""for tile in bmpreader.read_n_bytes(all_tiles, 16):
		if char_dict.get(tile) is None:
			#print struct.unpack('<8H', tile)
			char_dict[tile] = struct.pack('>H', tile_idx)
			char_str = char_str + tile
			tile_idx = tile_idx + 1"""
	
	outchar_arrayname = charprefix + outchar_filename
	char_outname = outchar_path + os.path.sep + outchar_filename_ext	
	chararray_writer.write_file(char_outname, char_str, outchar_arrayname, 2048*8)
	
	for (bmpfile, index) in zip(bmp_in, range(0, len(vb_scene))):
		bmp_path, bmp_filename_ext = os.path.split(bmpfile)
		bmp_filename = os.path.splitext(bmp_filename_ext)[0]
		bmp_arrayname = bgprefix + bmp_filename
		#bmp_outname = bmp_path + os.path.sep + bmp_filename + ".c"
		
		#BMP C file side effects are output into the same directory as
		#the char file.
		bmp_outname = os.path.join(outchar_path, bmp_filename + ".c")
		
		#bgindex = ''
		#for tile in bmpreader.read_n_bytes(bgmap, 16):
		#	print struct.unpack('>H', char_dict[tile])
		#	bgindex = bgindex + char_dict[tile]
		bg_str = vb_scene.bg_raw(index)	
		bgarray_writer.write_file(bmp_outname, bg_str, bmp_arrayname)
		
		#bmpreader.extract_palettes_and_indices(f_str)
		
		#write_array_short(bmp_outname, bmp_arrayname, f_str)
		
	#print "Creating char array " + charprefix + outchar_filename + " at " + outchar_path + os.path.sep + outchar_filename + ".c"
		
	
"""def extract_palettes_and_indices(bmp_stream):	
	pass

#http://stackoverflow.com/questions/3753589/packing-and-unpacking-variable-length-array-string-using-the-struct-module-in-py
def unpack_helper(fmt, data):
	size = struct.calcsize(fmt)
	return struct.unpack(fmt, data[:size])"""
	
if __name__ == '__main__':
	parser = optparse.OptionParser(usage="Usage: %prog [options] bmp1 [bmp2 ...]")
	parser.add_option("-b", None, action="store",  type="string", \
		dest="bgprefix", help="Array prefix for background files", default="bg_")
	parser.add_option("-c", None, action="store",  type="string", \
		dest="charprefix", help="Array prefix for character file.", default="char_")
	#parser.add_option("-p", None, action="store",  type="string", \
	#	dest="outprefix", help="File name prefix for output background files (not prepended to array names).", default="")
	#Header option?
	parser.add_option("-x", None, action="store_true", dest="compress", \
		 help="Compress character maps and BGs (default: %default)", default=True)
	parser.add_option("-o", None, action="store", type="string", \
		dest="charfile", help="Output character file (default: Name of first bitmap, prefixed with 'c')", default=None)
	(options, args) = parser.parse_args()
	
	if not args:
		print "No input files specified. Aborting."
		exit(-2)
		
	bmp2vbch_cmd(args, options.charfile, options.compress, options.bgprefix, options.charprefix)