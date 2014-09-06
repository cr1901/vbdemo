import os

vars = Variables(['variables.cache', 'settings.py'])
vars.AddVariables( \
	('AS', 'The Virtual Boy (GNU) assembler', 'v810-as'), \
	('CC', 'The Virtual Boy C compiler', 'v810-gcc'), \
	('LINK', 'The Virtual Boy linker (defaults to compiler driver)', 'v810-gcc'), \
	('OBJCOPY', 'The Virtual Boy object copier', 'v810-objcopy'), \
	PathVariable('GCCVB_DIR', 'Path to GCCVB bin dir (if not on standard SCons paths)', None), \
	PathVariable('RETROARCH_DIR', 'Path to RetroArch dir (if not on standard SCons paths)', None), \
	#PathVariable('RETROARCH_DIR', 'Path to RetroArch VB core (if not on standard SCons paths)', \
		#Dir('mednafen_vb_libretro'), PathVariable.PathAccept) #Error- hmmm... \
	PathVariable('RETROARCH_CORE', 'Path to RetroArch VB core (if not on standard SCons paths)', \
		File('mednafen_vb_libretro'), PathVariable.PathAccept) \
	)


#env = Environment(tools = ['as', 'cc', 'link'], variables = vars)

if os.name == 'nt':
	env = Environment(tools = ['mingw'], variables = vars)
else:
	env = Environment(tools = ['gcc'], variables = vars)

vars.Save('variables.cache', env)
Help(vars.GenerateHelpText(env))

for extra_path in ['GCCVB_DIR', 'RETROARCH_DIR']:
	try:
		env.AppendENVPath('PATH', env[extra_path])
	except KeyError:
		pass


objcopy = Builder(action = '$OBJCOPY $OBJCOPYFLAGS $SOURCE $TARGET', \
	suffix = '$BINSUFFIX', src_suffix = '.elf')
#binary = Builder(action = '$CC -o $TARGET -Wl,-r $CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES', \
#	suffix = '$PROGSUFFIX', src_suffix = '.c')

env['CCFLAGS'] = '-Wall -nodefaultlibs -mv810 -xc'
env['CPPPATH'] = ['#/include', '#/assets', '#/external']
#env['LINKFLAGS'] = '-r' #Just use the compiler driver for now...
env['PROGSUFFIX'] = '.elf'

#env['BUILDERS']['Binary'] = binary
env['BUILDERS']['Objcopy'] = objcopy
env['OBJCOPYFLAGS'] = '-S -O binary'
env['BINSUFFIX'] = '.vb'


SConscript('external/SConscript', exports = ['env'])
Import('env') #We need to get the exported environment back...
ROMfile = SConscript('src/SConscript', exports = ['env']) #Just to pass it into something else!

#print env.WhereIs('v810-gcc')
#env.AppendENVPath('PATH', ARGUMENTS.get('GCCVB_DIR', ''))
#env['AS'] = 'VBASM'
#env['ASCOM'] = '$AS $ASFLAGS $SOURCES -o $TARGET'
#env['OBJSUFFIX'] = '.vb'

#libretro_core = libretro_base.File('cores/mednafen_vb_libretro.dll')
#
#ROMfile = env.Object('vbdemo.vb', 'vbmain.asm')
testROM = env.Command('testROM', ROMfile, \
	Action([['retroarch', '${SOURCE.abspath}', '-L', '$RETROARCH_CORE']]), \
	chdir = env['RETROARCH_DIR'])
#
#Default(libgccvb)
Default(ROMfile)
