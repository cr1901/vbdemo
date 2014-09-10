#ifndef GAMEMODE_H
#define GAMEMODE_H

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


#endif        /*  #ifndef GAMEMODE_H  */

