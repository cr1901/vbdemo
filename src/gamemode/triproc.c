#include "libgccvb/libgccvb.h"
#include "gamectl.h"
#include <limits.h>



typedef struct vb_point
{
	short x;
	short y;
	short parallax;
}VB_POINT;

volatile int frame_begin = 0;

int frame_has_begun();
void vpu_int(void);
void draw_line(VB_POINT pstart, VB_POINT pend);
void inline plot_point(VB_POINT p);
VB_POINT inline create_point(short x, short y, short parallax);
/* void inline convert_octant(short * dx, short * dy, short * z); */
int sign(int i);
int iabs(int i);
//int swap(short * x, short * y);


void triangle_mainproc()
{
	WA[31].head = WRLD_END;
	vbDisplayShow();
	int poly_count;
	
	/* Bind vector to routine */
	vpu_vector = (unsigned long) vpu_int;
	frame_begin = 0;
	
	VIP_REGS[INTENB] = 0;
	VIP_REGS[INTENB] |= XPEND;
	
	while(!(vbPadKeyDown()))
	{
		//int i;
		/* for(i = 0; i < 384; i++)
		{
			plot_point(i, i, i/12);
		} */
		//Synchronize with display
		while(!frame_has_begun());
		
		//Draw lines until VIP says that "need to draw"
		
		//Worst case performance test
		/* 
		draw_line(create_point(0, 0, 0), create_point(383, 223, 0));
		draw_line(create_point(0, 0, 0), create_point(383, 223, 0));
		draw_line(create_point(0, 0, 0), create_point(383, 223, 0));
		*/
		
		
		/* Bresenham test pattern */
		/* abs(tan(x/y)) = 0.26 (15 degrees) */
		draw_line(create_point(192, 112, 0), create_point(383, 62, 0));
		draw_line(create_point(192, 112, 0), create_point(0, 62, 0));
		draw_line(create_point(192, 112, 0), create_point(0, 162, 0));
		draw_line(create_point(192, 112, 0), create_point(383, 162, 0));
		
		/* abs(tan(x/y)) = sqrt(3) */
		draw_line(create_point(192, 112, 0), create_point(258, 0, 0));
		draw_line(create_point(192, 112, 0), create_point(126, 0, 0));
		draw_line(create_point(192, 112, 0), create_point(126, 223, 0));
		draw_line(create_point(192, 112, 0), create_point(258, 223, 0));
		
		/* abs(tan(x/y)) = 1/sqrt(3) (About equal to aspect ratio) */
		draw_line(create_point(192, 112, 0), create_point(383, 0, 0));
		draw_line(create_point(192, 112, 0), create_point(0, 0, 0));
		draw_line(create_point(192, 112, 0), create_point(0, 223, 0));
		draw_line(create_point(192, 112, 0), create_point(383, 223, 0));
                
		/* Vertical/horizontal */
		draw_line(create_point(192, 112, 0), create_point(383, 112, 0));
		draw_line(create_point(192, 112, 0), create_point(192, 0, 0));
		draw_line(create_point(192, 112, 0), create_point(0, 112, 0));
		draw_line(create_point(192, 112, 0), create_point(192, 223, 0));
		
		
		
		/* Bresenham test pattern */
		/* abs(tan(x/y)) = 0.26 (15 degrees) */
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {383, 62, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {0, 62, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {0, 162, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {383, 162, 0});
		//
		///* abs(tan(x/y)) = sqrt{3} */
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {258, 0, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {126, 0, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {126, 223, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {258, 223, 0});
		//
		///* abs(tan(x/y)) = 1/sqrt{3} (About equal to aspect ratio) */
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {383, 0, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {0, 0, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {0, 223, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {383, 223, 0});
                //
		///* Vertical/horizontal */
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {383, 112, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {192, 0, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {0, 112, 0});
		//draw_line((VB_POINT) {192, 112, 0}, (VB_POINT) {192, 223, 0});
		
		
		//draw_line(create_point(0, 0, 0), create_point(383, 223, 0));
		//draw_line(create_point(0, 0, 0), create_point(383, 223, 0));
		//poly_count++;
	}
	 
	
	vbDisplayHide();
	jump_to_reset();
}

//Use Bresenham's algorithm
void draw_line(VB_POINT pstart, VB_POINT pend)
{
	VB_POINT pcurr;
	int do_swap = 0; /* Iterate over Y if 1 */
	//int do_reverse = 0;  /* End point < Start point if 1 */
	short dx, dy;
	//short di; /* Change in independent var */
	//short dd; /* Change in dependent var */
	//short curr_dv, start_iv, end_iv, start_dv, end_dv;
	//short * curr_x, * curr_y;
	
	dx = iabs(pend.x - pstart.x);
	dy = iabs(pend.y - pstart.y); 
	
	/* If y changes at a faster rate than y, do all calculations relative to
	y (i.e. y is independent var), and reverse vars when plotting. */
	do_swap = (dx < dy);
	
	//error = 2*dd - di;
	
	plot_point(pstart);
	pcurr = pstart;
	
	/* X is independent var */
	if(!do_swap && (pend.x >= pstart.x))
	{
		long error = 2*dy - dx;
		while(++pcurr.x <= pend.x)
		{
			if(error > 0)
			{
				if(pend.y > pstart.y)
				{
					pcurr.y = pcurr.y + 1;
				}
				else
				{
					pcurr.y = pcurr.y - 1;
				}
				
				error += (2*dy - 2*dx);
			}
			else
			{
				error += 2*dy;
			}
			
			plot_point(pcurr);
		}
	}
	else if(!do_swap && (pend.x <= pstart.x))
	{
		long error = 2*dy - dx;
		while(--pcurr.x >= pend.x)
		{
			if(error > 0)
			{
				if(pend.y > pstart.y)
				{
					pcurr.y = pcurr.y + 1;
				}
				else
				{
					pcurr.y = pcurr.y - 1;
				}
				
				error += (2*dy - 2*dx);
			}
			else
			{
				error += 2*dy;
			}
			
			plot_point(pcurr);
		}
	}
	
	/* Y is independent var */
	else if(do_swap && (pend.y > pstart.y))
	{
		long error = 2*dx - dy;
		while(++pcurr.y <= pend.y)
		{
			if(error > 0)
			{
				if(pend.x > pstart.x)
				{
					pcurr.x = pcurr.x + 1;
				}
				else
				{
					pcurr.x = pcurr.x - 1;
				}
				
				error += (2*dx - 2*dy);
			}
			else
			{
				error += 2*dx;
			}
			
			plot_point(pcurr);
		}
	}
	else if(do_swap && (pend.y < pstart.y))
	{
		long error = 2*dx - dy;
		while(--pcurr.y >= pend.y)
		{
			if(error > 0)
			{
				if(pend.x > pstart.x)
				{
					pcurr.x = pcurr.x + 1;
				}
				else
				{
					pcurr.x = pcurr.x - 1;
				}
				
				error += (2*dx - 2*dy);
			}
			else
			{
				error += 2*dx;
			}
			
			plot_point(pcurr);
		}
	}
}

void inline plot_point(VB_POINT p)
{
	short y_bias = 2*(p.y & 0x0F); /* Multiply by 2 b/c 2 bits == 1 pixel */
	
	//short rx_offs = 16*(p.x);
	//short lx_offs = 16*(p.x);
	short rx_offs = 16*(p.x + p.parallax); /* 64 bytes (half-words) per column == 16 longs */
	short lx_offs = 16*(p.x - p.parallax); /* 64 bytes (half-words) per column == 16 longs */
	short y_offs = p.y >> 4; /* 16 pixels per 4 bytes (doubleword). */
	short lframe_pos = lx_offs + y_offs;
	short rframe_pos = rx_offs + y_offs;
		
	(* (L_FRAME0 + lframe_pos)) |= 0x0003uL << y_bias;
	(* (L_FRAME1 + lframe_pos)) |= 0x0003uL << y_bias;
	(* (R_FRAME0 + rframe_pos)) |= 0x0003uL << y_bias;
	(* (R_FRAME1 + rframe_pos)) |= 0x0003uL << y_bias;	
}

int sign(int i)
{
	return i > 0 ? 1 : -1;
}

/* Relies on twos-complement arithmetic. */
int iabs(int i)
{
	return i >= 0 ? i : -i;
}

VB_POINT inline create_point(short x, short y, short parallax)
{
	VB_POINT p;
	p.x = x;
	p.y = y;
	p.parallax = parallax;
	return p;	
}

int frame_has_begun()
{
	if(frame_begin == 1)
	{
		frame_begin = 0;
		return 1;
	}
	else
	{
		return 0;
	}
}

void vpu_int()
{
	frame_begin = 1;
	VIP_REGS[INTCLR] |= XPEND;
}
/* void inline convert_octant(short * dx, short * dy, short * z)
{
	if(	
	
} */
