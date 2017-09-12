#ifndef TIMEDRIV_H
#define TIMEDRIV_H

#include <libgccvb.h>


#define MAX_NUM_TIMERS 32

typedef struct timer_observer
{
	void (* notify_fcn)(volatile void *);
	volatile void * target_data;
}TIMER_OBSERVER;

/* typedef struct timer_subject
{

}TIMER_SUBJECT; */

typedef struct comparator
{
	TIMER_OBSERVER notifier;
	int in_use;
	unsigned short ticks_elapsed;
	unsigned short ticks_target;
}COMPARATOR;



/* For now, changing the timer granularity is impossible on demand. */
/* typedef enum vb_timer_gran
{
	VB_TIMER_20_MICRO,
	VB_TIMER_100_MICRO
}VB_TIMER_GRAN; */


/* void set_physical_timer_granularity(VB_TIMER_GRAN gran);
void set_interrupt_granularity(unsigned short target_ticks); */
int set_timer_to_inuse(unsigned short target_ticks, void (*)(volatile void *), volatile void *);
void unset_timer_from_inuse(int index);
void bind_tim_vector();
void init_timer_hw();
void stop_timer_and_int();

extern unsigned long tim_vector; /* Embedded in libgccvb's runtime. */



#endif        /*  #ifndef TIMEDRIV_H  */
