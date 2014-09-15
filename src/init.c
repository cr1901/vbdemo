#include "gamectl.h"
#include "intrupt/timeint.h"
#include "libgccvb/libgccvb.h"

GAME_MODE initial_game_mode;
int init_just_occurred;

static void setup_intvecs();

void init_video()
{
	vbDisplayOn();
	vbSetColTable();
}

void init_vb()
{
	setup_intvecs();
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

void setup_intvecs()
{	
	/* Set up interrupt vectors. In reality, this is ROM. These assignments 
	are Undefined in ANSI (cannot convert fcn ptr to data "ptr")- nothing 
	can be done about this. This code will need to be rewritten for 
	compilation with VUCC. */
	tim_vector = (u32)(timer_handler);
	
}
