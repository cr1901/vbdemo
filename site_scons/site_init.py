import os.path

def tool_add_objcopy(env):
	objcopy_bld = Builder(action = '$OBJCOPY $OBJCOPYFLAGS $SOURCE $TARGET', \
		suffix = '$BINSUFFIX', src_suffix = '.elf') 
	env['OBJCOPYFLAGS'] = '-S -O binary'
	env['BINSUFFIX'] = '.vb'
	env.Append(BUILDERS = {'Objcopy' : objcopy_bld})
	
def tool_add_padROM(env):
	padROM_bld = Builder(action = '$PAD $SOURCE 0 21 $TARGET', suffix='.vb', \
		src_suffix = '.vb', emitter=modify_targets)
	env.Append(BUILDERS = {'PadROM' : padROM_bld})

#The padder will require an emitter to change the default target output name.
def modify_targets(target, source, env):
	filename, ext = os.path.splitext(str(target[0]))
	target = [filename + '_pad' + ext]
	return target, source	
	
def tool_add_flashROM(env):
	flashROM_bld = Builder(action = '$FLASH $SOURCE', src_suffix = '.vb')
	env.Append(BUILDERS = {'FlashROM' : flashROM_bld})
	
#def tool_add_buildassets(env):
#	buildasset_bld
	
#binary = Builder(action = '$CC -o $TARGET -Wl,-r $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES', \
#	suffix = '$PROGSUFFIX', src_suffix = '.c')

#env['BUILDERS']['Binary'] = binary
