import os.path

def tool_add_objcopy(env):
	objcopy_bld = Builder(action = '$OBJCOPY $OBJCOPYFLAGS $SOURCE $TARGET', \
		suffix = '$BINSUFFIX', src_suffix = '.elf') 
	env['OBJCOPYFLAGS'] = '-S -O binary'
	env['BINSUFFIX'] = '.vb'
	env.Append(BUILDERS = {'Objcopy' : objcopy_bld})
	
	
"""SCons manual: If the suffix is a string, then scons will append a 
'.' to the beginning of the suffix if it's not already there. The 
string returned by callable object (or obtained from the dictionary) is 
untouched and must append its own '.' to the beginning if one 
is desired."""	
def tool_add_padROM(env):
	padROM_bld = Builder(action = '$PAD $SOURCE 0 21 $TARGET', \
		suffix={None: '_pad.vb'}, src_suffix = '.vb')
	env.Append(BUILDERS = {'PadROM' : padROM_bld})
	
def tool_add_flashROM(env):
	flashROM_bld = Builder(action = '$FLASH $SOURCE', src_suffix = '.vb')
	env.Append(BUILDERS = {'FlashROM' : flashROM_bld})
	
def tool_add_buildassets(env):
	buildasset_bld = Builder(generator = decide_asset_builder, \
		src_suffix = ['.c', '.asm'], prefix='g', suffix='.c', \
		single_source=True)
	env.Append(BUILDERS = {'BuildAssets' : buildasset_bld})
			
def noop(target = None, source = None, env = None):
	return 0
	
	
	
def decide_asset_builder(source, target, env, for_signature):
	filename, ext = os.path.splitext(str(source[0]))
	if ext == '.c':
		return Copy(target[0], source[0])

#def pybin2C(source, target, env):
#	with open(source) as binfile:
#		bin_data = binfile.read()
#		
#	with open(target, 'w') as cfile:
		
	
	
#binary = Builder(action = '$CC -o $TARGET -Wl,-r $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES', \
#	suffix = '$PROGSUFFIX', src_suffix = '.c')

#env['BUILDERS']['Binary'] = binary
