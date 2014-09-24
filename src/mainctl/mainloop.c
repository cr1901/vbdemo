#include "gamectl.h"

void main_loop()
{
	/* Todo: Is this in fact necessary? The only place this can be called
	is in fact AFTER init... */
	static GAME_MODE curr_game_mode;
	
	if(init_just_occurred)
	{
		curr_game_mode = initial_game_mode;
		init_just_occurred = 0;
	}
	
	for(;;)
	{
		/* Mode independent processing goes here. */
		
		/* Mode-change dependent processing (call mode setup routine) or 
		Run mode mainproc. */
		
		/* Each mode should have at least 3 main files: mainproc, setup, 
		and interrupt processing. */
		mode_main_jump_table[curr_game_mode]();
	}
}
