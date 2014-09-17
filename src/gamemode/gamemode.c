#include <stddef.h> /* Any conforming C compiler will have this... */
#include "gamectl.h"

GAME_STATE curr_game_state;

game_mode_main_sub_t mode_main_jump_table[] = {
	focus_screen_mainproc,
	affine_demo_mainproc,
	triangle_mainproc
};
