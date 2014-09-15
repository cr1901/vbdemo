import os

vars = Variables(['variables.cache', 'settings.py'])
vars.AddVariables( \
	('AS', 'The Virtual Boy (GNU) assembler', 'v810-as'), \
	('CC', 'The Virtual Boy C compiler', 'v810-gcc'), \
	('LINK', 'The Virtual Boy linker (defaults to compiler driver)', 'v810-gcc'), \
	('OBJCOPY', 'The Virtual Boy object copier', 'v810-objcopy'), \
	('PAD', 'The Virtual Boy padding tool', 'Pad_VB'), \
	('FLASH', 'The Virtual Boy object copier', 'FlashBoy'), \
	BoolVariable('VUCC_COMPAT', 'Set to generate a batch file which can be used with Virtual Utopia C Compiler (Nonfunctional!)', False), \
	PathVariable('GCCVB_DIR', 'Path to GCCVB bin dir (if not on standard SCons paths)', None), \
	PathVariable('RETROARCH_DIR', 'Path to RetroArch dir (if not on standard SCons paths)', None), \
	#PathVariable('RETROARCH_DIR', 'Path to RetroArch VB core (if not on standard SCons paths)', \
		#Dir('mednafen_vb_libretro'), PathVariable.PathAccept) #Error- hmmm... \
	PathVariable('RETROARCH_CORE', 'Path to RetroArch VB core (if not on standard SCons paths)', \
		File('mednafen_vb_libretro'), PathVariable.PathAccept), \
	PathVariable('PAD_DIR', 'Path to VB padding tool (if not on standard SCons paths)', None), \
	PathVariable('FLASH_DIR', 'Path to VB flashing tool (if not on standard SCons paths)', None) \
	)

#env = Environment(tools = ['as', 'cc', 'link'], variables = vars)
if os.name == 'nt':
	env = Environment(tools = ['mingw', tool_add_objcopy, tool_add_padROM, \
		tool_add_flashROM, tool_add_buildassets], variables = vars)
else:
	env = Environment(tools = ['gcc', tool_add_objcopy, tool_add_padROM, \
		tool_add_flashROM, tool_add_buildassets], variables = vars)

vars.Save('variables.cache', env)
Help(vars.GenerateHelpText(env))

for extra_path in ['GCCVB_DIR', 'RETROARCH_DIR', 'PAD_DIR', 'FLASH_DIR']:
	try:
		env.AppendENVPath('PATH', env[extra_path])
	except KeyError:
		pass
	
if env['VUCC_COMPAT']:
	env.Append(CPPDEFINES='USING_VUCC')
	SetOption('no_exec', True)	

env['CCFLAGS'] = '-Wall -nodefaultlibs -mv810 -xc'
env['CPPPATH'] = ['#/include', '#/external']
#env['LINKFLAGS'] = '-r' #Just use the compiler driver for now...
env['PROGSUFFIX'] = '.elf'

SConscript('external/SConscript', exports = ['env'])
Import('env') #We need to get the exported environment back...
ROMfile = SConscript('src/SConscript', exports = ['env']) #Just to pass it into something else!

testROM = env.Command('testROM', ROMfile, \
	Action([['retroarch', '${SOURCE.abspath}', '-L', '$RETROARCH_CORE']]), \
	chdir = env['RETROARCH_DIR'])

hwROM = env.PadROM(ROMfile)
flashROM = env.FlashROM(hwROM)
Alias('flashROM', flashROM)


Default(ROMfile)
