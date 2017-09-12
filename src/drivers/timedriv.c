#include <libgccvb.h>

#include "backend/timedriv.h"

//static unsigned long in_use_index;
static COMPARATOR timer_array[MAX_NUM_TIMERS];

/* static int precise_timer_on;
unsigned char precise_timer_int_cnt = 0; */

static void timer_handler();
static void clear_comparators();
static void run_inuse_comparators();
static int find_free_comparator();
//static void run_callbacks();

static void timer_handler()
{
	//if(precise_timer_on)
	//{
	//precise_timer_int_cnt++;
	//}

	run_inuse_comparators();

	/* Run one frame of sound driver here. */

	/* Run other observers if necessary? Or keep in
	run_inuse_comparators()? */

	/* VB manual recommends this. */
	HW_REGS[TCR] &= ~TIMER_INT;
	HW_REGS[TCR] |= TIMER_ZCLR;
	HW_REGS[TCR] |= TIMER_INT;
}

static void clear_comparators()
{
	register int count;
	for(count = 0; count < MAX_NUM_TIMERS; count++)
	{
		timer_array[count].in_use = 0;
	}
}

static void run_inuse_comparators()
{
	register int count;
	for(count = 0; count < MAX_NUM_TIMERS; count++)
	{
		if(timer_array[count].in_use)
		{
			timer_array[count].ticks_elapsed++;
			if(timer_array[count].ticks_elapsed > timer_array[count].ticks_target)
			{
				timer_array[count].ticks_elapsed = 0;

				/* If the desired time has elapsed, modify the target
				data using the callback. */
				timer_array[count].notifier.notify_fcn( \
					timer_array[count].notifier.target_data);
			}
		}
	}
}



static int find_free_comparator()
{
	register int count = 0;
	/* We need to find a timer that is not currently in use. */

	while(count < MAX_NUM_TIMERS && timer_array[count++].in_use)
	{
		/* That's the whole loop :D. */
	}

	return (count < MAX_NUM_TIMERS) ? count : -1;
}


/* This should be "atomic" in the sense that the timer is not "in use" until
after all data is set up. */
int set_timer_to_inuse(unsigned short target_ticks, void (* callback)(volatile void *), volatile void * data)
{
	int index;

	/* We need to find a timer that is not currently in use. */
	if((index = find_free_comparator()) >= 0)
	{
		timer_array[index].ticks_target = target_ticks;
		timer_array[index].ticks_elapsed = 0;
		timer_array[index].notifier.target_data = data;
		timer_array[index].notifier.notify_fcn = callback;
		timer_array[index].in_use = 1;
	}

	return index;
}

void unset_timer_from_inuse(int index)
{
	timer_array[index].in_use = 0;

}

/* Required because the interrupt vectors for VB are embedded into the
stub crt0. */
void bind_tim_vector()
{
	tim_vector = (unsigned long) timer_handler;
}


void init_timer_hw()
{
	clear_comparators(); /* Makes sure nothing is in use. */

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
