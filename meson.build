project('vbdemo', 'c')
cc = meson.get_compiler('c')

if not meson.is_cross_build() or not (host_machine.cpu() == 'v810')
    error('Inappropriate environment for compiling vbdemo')
endif

bmp2vbch = find_program(['tools/bmp2vbch.py'])
objcopy = find_program('v810-objcopy')
retroarch = find_program('retroarch', required : false)
# padvb = find_program('P')
# flashboy

subdir('external')
subdir('src')
subdir('assets')

elffile = executable('vb_demo', vbdemo_src, name_suffix : 'elf',
    link_with : libgccvb,
    include_directories : [vbdemo_incdir, libgccvb_incdir],
    c_args : '-DINITIAL_GAME_MODE=' + get_option('start_mode'))
binfile = custom_target('vb_demo.bin',
    command : [objcopy, '-S', '-O', 'binary', '@INPUT@', '@OUTPUT@'],
    input : elffile,
    output : 'vb_demo.bin',
    build_by_default : true)
# padrom =

if retroarch.found()
    custom_target('test_rom',
        command : [retroarch, '-L', get_option('retroarch_core'), '@INPUT@'],
        input : binfile,
        output : 'test_rom',
        build_by_default : false)
endif
