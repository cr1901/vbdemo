#include "gamectl.h"
#include "libgccvb/libgccvb.h"

GAME_MODE initial_game_mode;
int init_just_occurred;

void init_video()
{
	vbDisplayOn();
	vbSetColTable();
}

void init_vb()
{
	init_video();
	vbDisplayHide();
	curr_game_state = SETUP; /* Really inelegant, but it'll do for now. */
	initial_game_mode = FOCUS_SCREEN;
	init_just_occurred = 1;	
}

void inline jump_to_reset()
{
	jump_addr((void *) 0xFFFFFFF0);
}

