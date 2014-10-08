import os.path

from vb_py.bmp2vbch import bmp2vbch_cmd

#===============================================================================
#Custom tools.
#===============================================================================
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

#Possible the tool is no longer necessary, but kept just in case.
#Strangely, the Copy() function chokes if attempting to return an Action
#(SCons executable unit) without inputting parameters.
def tool_add_movesource(env):
	pass
	"""movesource_bld = Builder(action = Copy("$TARGET", "$SOURCE"), \
		src_suffix = ['.c', '.asm'], prefix='g', \
		single_source=True)
	env.Append(BUILDERS = {'MoveSource' : movesource_bld})"""

def tool_add_bmp2vbch(env):
	#buildasset_bld = Builder(action = bmp2vbch_scons, prefix='g', \
	buildasset_bld = Builder(action = bmp2vbch_scons, \
		suffix='.c', single_source=False)
	env.Append(BUILDERS = {'BMP2VBch' : buildasset_bld})	

#Determine whether really needed. Would remove the need for SideEffects, but
#causes more files to be generated, and would require some rework of
def tool_add_vbch2C(env):
	pass
	#vbch2C_bld = 
	
def tool_add_vbbg2C(env):
	pass


#===============================================================================
#SCons wrappers for Python functions to execute.
#===============================================================================
def bmp2vbch_scons(target, source, env):
	str_src = []
	for src in source:
		str_src.append(str(src))
	bmp2vbch_cmd(str_src, charfile=str(target[0]))
	
#===============================================================================
#Helper functions.
#===============================================================================
#SCons/Make is ill-suited for multiple targets...

"""def add_targets(target=None, source=None, env=None):
	#for src in source:
	#	trg_head = os.path.split(str(target))[0]
	#	tail = os.path.split(str(src))[1]
	#	filename = os.path.splitext(tail)[0]
	#	target.append(os.path.join(trg_head,'g' + filename + '.c'))
	return target, source"""
	
def create_SideEffect_names(target_list, source_list, prefix = '', suffix = ''):
	side_effect_list = []
	target_dir = File(target_list[0]).Dir('.')
	for src in source_list:
		tail = os.path.split(str(src))[1]
		filename = os.path.splitext(tail)[0]
		side_effect_list.append(target_dir.File(prefix + filename + suffix))
	return side_effect_list
	
			
"""def noop(target = None, source = None, env = None):
	return 0"""
	
	
	
"""def decide_asset_builder(source, target, env, for_signature):
	filename, ext = os.path.splitext(str(source[0]))
	if ext == '.c':
		return Copy(target[0], source[0])"""

#def pybin2C(source, target, env):
#	with open(source) as binfile:
#		bin_data = binfile.read()
#		
#	with open(target, 'w') as cfile:
		
	
	
#binary = Builder(action = '$CC -o $TARGET -Wl,-r $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES', \
#	suffix = '$PROGSUFFIX', src_suffix = '.c')

#env['BUILDERS']['Binary'] = binary
