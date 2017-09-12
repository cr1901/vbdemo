libgccvb_incdir = include_directories('libgccvb')

src = ['affine.c', 'asm.c', 'audio.c', 'hw.c', 'joypad.c',
        'mem.c', 'misc.c', 'object.c', 'random2.c', 'timer.c',
        'video.c', 'vip.c', 'world.c']

libgccvb_src = []
foreach p : src
    libgccvb_src += join_paths('libgccvb', p)
endforeach

libgccvb = static_library('gccvb', libgccvb_src,
    include_directories : libgccvb_incdir,
    pic : false)
