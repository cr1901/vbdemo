#include "init.h"
#include "gamemode.h" /* For idempotency... I do this a lot. */
#include "libgccvb/libgccvb.h"

GAME_MODE initial_game_mode;
int init_just_occurred;

/* Can this fail? */
int init_video()
{
	vbDisplayOn();
	vbSetColTable();
	return 0;
}

void init_vb()
{
	init_video();
	vbDisplayHide();
	curr_game_state = SETUP; /* Really inelegant, but it'll do for now. */
	initial_game_mode = AFFINE_DEMO;
	init_just_occurred = 1;	
}

void inline jump_to_reset()
{
	jump_addr((void *) 0xFFFFFFF0);
}
