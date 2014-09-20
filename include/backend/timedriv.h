#ifndef TIMEDRIV_H
#define TIMEDRIV_H

#include "libgccvb/libgccvb.h"


#define MAX_NUM_TIMERS 32

typedef struct comparator
{
	unsigned char ticks_elapsed;
	unsigned char ticks_target;
}COMPARATOR;

typedef enum vb_timer_gran
{
	VB_TIMER_20_MICRO,
	VB_TIMER_100_MICRO
}VB_TIMER_GRAN;


void set_physical_timer_granularity(VB_TIMER_GRAN gran);
void set_interrupt_granularity(unsigned short target_ticks);
COMPARATOR * add_timer_to_pool(unsigned char target_ticks);
int remove_timer_from_pool(COMPARATOR *);
void bind_tim_vector();
void init_timer_hw();
void stop_timer_and_int();

extern unsigned long tim_vector; /* Embedded in libgccvb's runtime. */



#endif        /*  #ifndef TIMEDRIV_H  */

