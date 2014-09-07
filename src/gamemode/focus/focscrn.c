
#include "libgccvb/libgccvb.h"
#include "graphics/cross.h"
#include "graphics/focscrn.h"


void focus_screen_mainproc()
{
	//copymem((void*)CharSeg0, (void*)cgx_sample, 512 * 2);
	//copymem((void*)CharSeg1, (void*)(cgx_sample + 512), 512 * 2);
	
	copymem((void *)0x78000, (void*)cgx_sample, 8192*2);
	copymem((void*)BGMap(0), (void*)scr_ipd_foc, 4096*2);
	
	//setmem((void*)BGMap(0), 0x00, 0x2000); /* Just use the zeroth char for all tiles */
	//copymem((void*)CharSeg0, (void*)char_line, 16); /* Only need to use 1 char! */
	
	WA[31].head = WRLD_LON;
	WA[31].gx    = 0;
	WA[31].gp    = 0; //No parallax for now.
	WA[31].gy    = 0;
	//WA[30].mx = 384/2;
	//WA[30].my = 224/2;
	WA[31].w = 383;
	WA[31].h = 223;
	WA[31].ovr = 0;
	WA[31].param = 0; /* Affine Parameters begins after BG 0 (0x1000*2+0x20000) */
	
	WA[30].head = WRLD_RON;
	WA[30].gx    = 0;
	WA[30].gp    = 0; //No parallax for now.
	WA[30].gy    = 0;
	//WA[30].mx = 384/2;
	//WA[30].my = 224/2;
	WA[30].w = 383;
	WA[30].h = 223;
	WA[30].ovr = 0;
	WA[30].param = 0; /* Affine Parameters begins after BG 0 (0x1000*2+0x20000) */
	
	WA[29].head = WRLD_END;
	
	vbDisplayShow();
	
	
	for(;;);
	
	
	
}
