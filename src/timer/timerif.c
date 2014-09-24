#include "intrface/timerif.h"
#include "backend/timedriv.h"


/* timer_handle_t request_timer(short centiseconds)
{
	
} */

timer_handle_t request_timer(short centiseconds, void (* callback)(volatile void *), volatile void * input_data)
{
	return set_timer_to_inuse(centiseconds, callback, input_data);
}

void remove_timer(timer_handle_t t_handle)
{
	unset_timer_from_inuse(t_handle);	
}

void init_timer_driver()
{
	bind_tim_vector();
	init_timer_hw();
}

void stop_timer_driver()
{
	stop_timer_and_int();
}

