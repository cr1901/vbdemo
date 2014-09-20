#include "libgccvb/libgccvb.h"

#include "backend/timedriv.h"




static unsigned long in_use_index;
static COMPARATOR timer_array[MAX_NUM_TIMERS];

static int precise_timer_on; 
unsigned char precise_timer_int_cnt = 0;

static void timer_handler();

void bind_tim_vector()
{
	tim_vector = (unsigned long) timer_handler;
}


void timer_handler()
{
	//if(precise_timer_on)
	//{
	precise_timer_int_cnt++;
	//}
	
	/* Run one frame of sound driver here. */
	
	/* VB manual recommends this. */
	HW_REGS[TCR] &= ~TIMER_INT;
	HW_REGS[TCR] |= TIMER_ZCLR;
	HW_REGS[TCR] |= TIMER_INT;
}

void init_timer_hw()
{
	/* Timer interrupt will fire once every 10ms. */
	HW_REGS[THR] = 0; /* Initial timer counter is 0xFFFF. However, the
	hardware will reload the timer with 0x0000 during the next tick.
	Mednafen does not emulate this. */
	HW_REGS[TLR] = TIME_MS(10);
	HW_REGS[TCR] = 	TIMER_100US | TIMER_INT | TIMER_ENB;
}

void stop_timer_and_int()
{
	HW_REGS[TCR] &= ~(TIMER_ENB | TIMER_INT);
	
}
