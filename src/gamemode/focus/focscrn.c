
#include "libgccvb/libgccvb.h"
//#include "graphics/cross.h"
#include "graphics/focscrn.h"
#include "graphics/font_pc.h"

#define ASCII_BIAS 0x30

static const char msg_warn[]="IMPORTANT: READ INSTRUCTION AND PRECAUTION BOOKLETS BEFORE OPERATING";

static void load_warning_scr();
static void load_ipdfoc_scr();
static void fade_and_wait();
static void print_message(const char * message, short bg_no, short x_pos, short y_pos, short font_bias);

/* The first thing that the user will see. */
void focus_screen_mainproc()
{
	
	
	
	//setmem((void*)BGMap(0), 0x00, 0x2000); /* Just use the zeroth char for all tiles */
	//copymem((void*)CharSeg0, (void*)char_line, 16); /* Only need to use 1 char! */
	
	/* Give time for mirrors to adjust... */
	
	load_warning_scr();
	fade_and_wait();
	load_ipdfoc_scr();
	fade_and_wait();
	//vbDisplayOn();
	
	for(;;);
	
	
	
}

void load_warning_scr()
{

	//setmem((void*)BGMap(0), 0x00, 0x2000); /* Just use the zeroth char for all tiles */
	//addmem((void*) BGMap(0), (void *) msg_warn, sizeof(msg_warn), 0xD0);
	//addmem((void*) BGMap(0), (void *) msg_warn, sizeof(msg_warn), 0);
	copymem((void *)0x78000, (void*)font_pc, 8192);
	WA[31].head = WRLD_ON;
	WA[31].gx    = 0;
	WA[31].gp    = 0; //No parallax for now.
	WA[31].gy    = 0;
	//WA[30].mx = 384/2;
	//WA[30].my = 224/2;
	WA[31].w = 383;
	WA[31].h = 223;
	WA[31].ovr = 0;
	WA[31].param = 0;
	
	print_message(msg_warn, 0, 1, 1, 0);
	
	
}

void load_ipdfoc_scr()
{
	/* Load focus screen tiles into memory. */
	copymem((void *)0x78000, (void*)cgx_sample, 8192*2);
	copymem((void*)BGMap(0), (void*)scr_ipd_foc, 4096*2);
	/* Reload the worlds to point to the appropriate.
	Screen. */
	WA[31].head = WRLD_LON;
	WA[31].gx    = 0;
	WA[31].gp    = 0; //No parallax for now.
	WA[31].gy    = 0;
	//WA[30].mx = 384/2;
	//WA[30].my = 224/2;
	WA[31].w = 383;
	WA[31].h = 223;
	WA[31].ovr = 0;
	WA[31].param = 0;
	
	WA[30].head = WRLD_RON;
	WA[30].gx    = 0;
	WA[30].gp    = 0; //No parallax for now.
	WA[30].gy    = 0;
	//WA[30].mx = 384/2;
	//WA[30].my = 224/2;
	WA[30].w = 383;
	WA[30].h = 223;
	WA[30].ovr = 0;
	WA[30].param = 0;
	
	WA[29].head = WRLD_END;
	
}

void fade_and_wait()
{
	vbFXFadeIn(3);
	while(!vbPadKeyDown());
	vbFXFadeOut(3);
}

void print_message(const char * message, short bg_no, short x_pos, short y_pos, short font_bias)
{
	unsigned short count;
	
	short initial_tile_pos = (y_pos*224) + x_pos;
	
	for(count = 0; message[count] != '\0'; count++)
	{
		/* Convert the ASCII character to a short that is an appropriate
		offset into the character table, and set the relevant tiles of the
		BGMap to display the appropriate tiles. */
		(* ((short *) BGMap(bg_no) + initial_tile_pos + count)) = (short) (message[count] + font_bias);
	}
}
