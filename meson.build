project('vbdemo', 'c')
cc = meson.get_compiler('c')

if not meson.is_cross_build() or not (host_machine.cpu() == 'v810')
    error('Inappropriate environment for compiling vbdemo')
endif

subdir('external')
subdir('src')

bmp2vbch = find_program(['tools/bmp2vbch.py'])
objcopy = find_program('v810-objcopy')
subdir('assets')

elffile = executable('vb_demo', vbdemo_src, name_suffix : 'elf',
    link_with : libgccvb,
    include_directories : [vbdemo_incdir, libgccvb_incdir])
binfile = custom_target('vb_demo.bin',
    command : [objcopy, '-S', '-O', 'binary', '@INPUT@', '@OUTPUT@'],
    input : elffile,
    output : 'vb_demo.bin',
    build_by_default : true)
