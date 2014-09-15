#ifndef GAMECTL_H
#define GAMECTL_H



void main_loop();

typedef enum game_mode
{
	FOCUS_SCREEN,
	AFFINE_DEMO
}GAME_MODE;

typedef enum game_state
{
	SETUP,
	NORMAL,
	INTERRUPT
}GAME_STATE;

typedef void (* game_mode_main_sub_t) ();
typedef void (* game_mode_setup_sub_t) ();
typedef void (* game_mode_int_sub_t) ();

extern game_mode_main_sub_t mode_main_jump_table[];
extern game_mode_int_sub_t timer_int_jump_table[];

extern GAME_STATE curr_game_state;
extern int autopause_enabled;

void focus_screen_mainproc();
void affine_demo_mainproc();

//extern game_mode_int_sub_t mode_int_jump_table[];

void init_video();
void init_vb();
void jump_to_reset(); /* No return */

/* Shared with main loop */
extern int init_just_occurred;
extern GAME_MODE initial_game_mode; /* This also permits the possibility of
starting in any game mode, or do something like XMen for Genesis 
("Reset the Computer") :D. Only changed in two places. The logic here is to
disturb as little workRAM as possible on reset. */


#endif        /*  #ifndef GAMECTL_H  */

