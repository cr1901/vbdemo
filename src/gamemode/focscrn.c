
#include "libgccvb/libgccvb.h"
//#include "graphics/cross.h"
#include "assets/graphics/focscrn.h"
#include "assets/graphics/font_pc.h"

#include "gamectl.h"
#include "intrface/timerif.h"

#define ASCII_BIAS 0x30
#define CENTER_X(_m) ((48 - _m) >> 1)
#define CENTER_Y(_m) ((28 - _m) >> 1)

static const char * msg_warn[]= {"IMPORTANT: READ INSTRUCTION", "AND PRECAUTION BOOKLETS", 
"BEFORE OPERATING"};

static void load_warning_scr();
static void load_ipdfoc_scr();
static void fade_and_wait();
static void print_message(const char * message, short bg_no, short x_pos, short y_pos, short font_bias);

static void set_true(volatile void *);

extern unsigned char precise_timer_int_cnt;
//static void print_center_message(const char * message, short bg_no, short y_pos, unsigned short msg_len);

/* The first thing that the user will see. */
void focus_screen_mainproc()
{
	timer_handle_t wait_timer;
	volatile int two_seconds_passed = 0; /* I wonder if this is undefined 
	behavior... as long as the variable doesn't go out of scope while the 
	timer's in effect, I should be okay... */
	
	
	//setmem((void*)BGMap(0), 0x00, 0x2000); /* Just use the zeroth char for all tiles */
	//copymem((void*)CharSeg0, (void*)char_line, 16); /* Only need to use 1 char! */
	
	/* Give time for mirrors to adjust... */
	
	load_warning_scr();
	vbDisplayShow();
	
	/* Failure of this function is grounds for halting the program! */
	wait_timer = request_timer(200, set_true, &two_seconds_passed);
	while(!(two_seconds_passed && vbPadKeyDown()));
	vbDisplayHide();
	remove_timer(wait_timer);
	
	load_ipdfoc_scr();
	fade_and_wait();
	//vbDisplayOn();
	
	//vbPadKeyDown();
	//while(vbPadKeyDown() != K_BTNS);
	
	jump_to_reset();
	
	
	
}

void load_warning_scr()
{

	copymem((void *)0x78000, (void*)font_pc, 8192);	
	/* Clear out any leftover characters from previous BG. */
	setmem((void*)BGMap(0), 0, 0x2000);
	
	WA[31].head = WRLD_ON;
	WA[31].gx    = 0;
	WA[31].gp    = 0; //No parallax for now.
	WA[31].gy    = CENTER_Y(5)*8;
	WA[31].mx = 0;
	WA[31].mp = 0;
	WA[31].my = 0;
	WA[31].w = 384;
	WA[31].h = (5*8 - 1);
	WA[31].ovr = 0;
	WA[31].param = 0;
	
	WA[30].head = WRLD_END;
	
	print_message(msg_warn[0], 0, CENTER_X(27), 0, 0);
	print_message(msg_warn[1], 0, CENTER_X(23), 2, 0);
	print_message(msg_warn[2], 0, CENTER_X(16), 4, 0);
	
	
}

void load_ipdfoc_scr()
{
	/* Load focus screen tiles into memory. */
	/* copymem((void *)0x78000, (void*)cgx_sample, 8192*2);
	copymem((void*)BGMap(0), (void*)scr_ipd_foc, 4096*2); */
	copymem((void *)0x78000, (void*)char_cfoc, 8192*2);
	copymem((void*)BGMap(0), (void*)bg_vblogo_r, 4096*2);
	copymem((void*)BGMap(1), (void*)bg_vblogo_l, 4096*2);
	
	/* Reload the worlds to point to the appropriate.
	Screen. */
	WA[31].head = WRLD_RON;
	WA[31].gx = 0;
	WA[31].gp = 1;
	WA[31].gy = 0;
	WA[31].mx = 0;
	WA[31].mp = 0;
	WA[31].my = 0;
	WA[31].w = 383;
	WA[31].h = 223;
	WA[31].ovr = 0;
	WA[31].param = 0;
	
	WA[30].head = WRLD_LON + 1;
	WA[30].gx    = 0;
	WA[30].gp    = 1; //No parallax for now.
	WA[30].gy    = 0;
	WA[30].mx = 0;
	WA[30].mp = 0;
	WA[30].my = 0;
	WA[30].w = 383;
	WA[30].h = 223;
	WA[30].ovr = 0;
	WA[30].param = 0;
	
	WA[29].head = WRLD_END;
	
}

void fade_and_wait()
{
	//vbFXFadeIn(3);
	vbDisplayShow();
	while(!vbPadKeyDown());
	vbDisplayHide();
	//vbFXFadeOut(3);
}

void set_true(volatile void * flag)
{
	(* (volatile int *) flag) = 1;
}



/* Limited to one segment... for now, anyway. */
/* No support for newlines, autowrapping... yet. */
/* Assumes: Display is off. */

/* Todo: turn into a text-box routine. */
void print_message(const char * message, short bg_no, short x_pos, short y_pos, short font_bias)
{
	unsigned short count;
	short initial_tile_pos = (y_pos*64) + x_pos;
	
	for(count = 0; message[count] != '\0'; count++)
	{
		/* Convert the ASCII character to a short that is an appropriate
		offset into the character table, and set the relevant tiles of the
		BGMap to display the appropriate tiles. */
		(* ((short *) BGMap(bg_no) + initial_tile_pos + count)) = (short) (message[count] + font_bias);
	}
}

/* void print_center_message(const char * message, short bg_no, short y_pos, unsigned short msg_len, short font_bias));
{
	short x_center = ((48 - msg_len) >> 1);
	
} */
