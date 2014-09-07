def tool_add_objcopy(env):
	objcopy_bld = Builder(action = '$OBJCOPY $OBJCOPYFLAGS $SOURCE $TARGET', \
		suffix = '$BINSUFFIX', src_suffix = '.elf') 
	env['OBJCOPYFLAGS'] = '-S -O binary'
	env['BINSUFFIX'] = '.vb'
	env.Append(BUILDERS = {'Objcopy' : objcopy_bld})
	
#def tool_add_buildassets(env):
#	buildasset_bld
	
#binary = Builder(action = '$CC -o $TARGET -Wl,-r $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES', \
#	suffix = '$PROGSUFFIX', src_suffix = '.c')

#env['BUILDERS']['Binary'] = binary
