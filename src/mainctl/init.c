#include "gamectl.h"
#include "intrface/timerif.h"
#include "intrface/sndplay.h"
#include "intrface/vidinit.h"
#include "libgccvb/libgccvb.h"

GAME_MODE initial_game_mode;
int init_just_occurred;

void init_vb()
{
	init_video_driver();
	init_timer_driver();
	/* init_sound_driver(); */
	curr_game_state = SETUP; /* Really inelegant, but it'll do for now. */
	initial_game_mode = FOCUS_SCREEN;
	init_just_occurred = 1;	
}

void inline jump_to_reset()
{
	INT_DISABLE;
	stop_timer_driver();
	jump_addr((void *) 0xFFFFFFF0);
}

