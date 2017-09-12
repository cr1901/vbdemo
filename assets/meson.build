src = ['cross.c', 'font_pc.c']

# Element 0 of each inner list is a target name for meson.
# Element 1 of each inner list is a set of input files to bmp2vbch.
# All images that should be share a char file should be part of the same list.
# Element 2 of each inner list is a set of output files from bmp2vbch.
# The first MUST be the character tile set created for the remaining outputs.
bmp = [
        [
            ['focus_screen'],
            ['vblogo_l.bmp', 'vblogo_r.bmp'],
            ['cfoc.c', 'vblogo_l.c', 'vblogo_r.c']
        ],
]

# Some gfx assets already exist.
c_char_files = []
foreach c : src
    c_char_files += join_paths('graphics', c)
endforeach

# Generate the remaining assets.
bmp_c_src = []
foreach b_set : bmp
    bmp_in = []

    foreach b_in : b_set[1]
        bmp_in += join_paths('graphics', b_in)
    endforeach
    bmp_out = b_set[2]

    bmp_c_src += custom_target('focus_screen',
        command : [bmp2vbch, '-o@OUTPUT0@', '@INPUT@'],
        input : bmp_in,
        output : bmp_out)
endforeach

vbdemo_src += [bmp_c_src, files(c_char_files)]


# TODO: Do sound effects here...
