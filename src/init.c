#include "gamectl.h"
#include "intrupt/handlers.h"
#include "libgccvb/libgccvb.h"

GAME_MODE initial_game_mode;
int init_just_occurred;

static void setup_intvecs(); /* Todo: Move to handlers header or 
interrupt-related source file? */

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
	/* initial_game_mode = INITIAL_GAME_MODE; */
	//initial_game_mode = TRI_DEMO;
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
	key_vector = (u32)(key_handler);
	tim_vector = (u32)(timer_handler);
	cro_vector = (u32)(cro_handler);
	com_vector = (u32)(com_handler);
	vpu_vector = (u32)(vip_handler);
}
