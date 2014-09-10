#ifndef INIT_H
#define INIT_H

#include "gamemode.h"


void init_video();
void init_vb();
void jump_to_reset(); /* No return */

/* Shared with main loop */
extern int init_just_occurred;
extern GAME_MODE initial_game_mode; /* This also permits the possibility of
starting in any game mode, or do something like XMen for Genesis 
("Reset the Computer") :D. Only changed in two places. The logic here is to
disturb as little workRAM as possible on reset. */


#endif        /*  #ifndef INIT_H */

