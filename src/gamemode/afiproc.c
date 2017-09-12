#include "gamectl.h"

#include <libgccvb.h>
#include "assets/graphics/cross.h"

static void setup_affine_demo();
static void waste_cycles();

void affine_demo_mainproc()
{
	switch(curr_game_state)
	{
	case SETUP:
		setup_affine_demo();
		curr_game_state = NORMAL;
	case NORMAL:
		waste_cycles();
	default:
		waste_cycles();
	}
}

void setup_affine_demo()
{
	int row_cnt;
	setmem((void*)BGMap(0), 0x00, 0x2000); /* Just use the zeroth char for all tiles */

	for(row_cnt = 0; row_cnt < 224; row_cnt++)
	{
		    short x_skip, x_offset;
		    char * copy_base = (char *) (BGMap(1) + (16*row_cnt)); /* Calculate the base once per loop. */

		    //copymem((void *) copy_base, (void*)cross_affine, 16); /* Most affine params stay constant per row. */
		    //(* (short *) (copy_base + 2)) = 0; /* Leave parallax alone for now. */

		    //(* (copy_base + 0)) = ((row_cnt/28) << 3); /* 13.3 */
		    (* (copy_base + 1)) = 0; /* 13.3 */ //Does nothing?

		    /* Y-coordinate should increment by row compared to original BG (1-to-1) */
		    (* (copy_base + 4)) = (row_cnt << 3); /* 13.3 */
		    (* (copy_base + 5)) = ((row_cnt & 0x7F) >> 3); /* 13.3 */ /* WHY is the top bit a sign bit?! */
		    //(* (copy_base + 4)) = 0;

		    /* X-inc per pixel- 7.9 */ /* However, change the increment value per row! */
		    //x_skip = (512 - ((row_cnt * 512)/224)); /* Decrements by 512 over time. */
		    x_skip = ((255 - row_cnt) << 2); /* 1-to-1 mapping between BG and what's drawn. */
		    x_offset = row_cnt << 3;
		    //x_offset = -(row_cnt << 3);
		    (* (short *) (copy_base + 0)) = x_offset;
		    (* (short *) (copy_base + 6)) = x_skip;
		    //(* (copy_base + 6)) = ((224 - row_cnt) * 5) >> 2;
		    //(* (copy_base + 7)) = ((224 - row_cnt) * 5) >> 6;
		    //(* (copy_base + 6)) = ((255-row_cnt) << 1);
		    //(* (copy_base + 7)) = (((255-row_cnt) & 0x7F) >> 7);

		    (* (short *) (copy_base + 8)) = 0; /* Y-inc */
		    //(* (copy_base + 7)) = ; /* X-inc-lo */
		    //(* (copy_base + 8)) = 0; /* Y-inc-hi */
		    //(* (copy_base + 9)) = 0; /* Y-inc-lo */
		    //copymem(copy_base + 10, (void*)cross_affine, 6);
	}

	copymem((void*)CharSeg0, (void*)char_line, 16); /* Only need to use 1 char! */

	//Setup worlds
	//(This uses structs to access world data, the old method using functions is commented out)
	//WA[31].head = (WRLD_ON /* | WRLD_AFFINE */ | WRLD_OVR | 0x01);  /* We don't want tiling? */ //Something odd happens... some tiles don't show...
	WA[31].head = (WRLD_ON | WRLD_AFFINE | WRLD_OVR);
	WA[31].gx    = 0;
	WA[31].gp    = 0; //No parallax for now.
	WA[31].gy    = 75; // Use 2/3s of the screen.
	//WA[30].mx = 384/2;
	//WA[30].my = 224/2;
	WA[31].w = 384;
	WA[31].h = 149;
	WA[31].ovr = 0;
	WA[31].param = 0x01000; /* Affine Parameters begins after BG 0 (0x1000*2+0x20000) */

	WA[30].head = WRLD_END;

	vbDisplayShow();
}

static void waste_cycles()
{
	for(;;);
}
