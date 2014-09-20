#include "intrface/timerif.h"
#include "backend/timedriv.h"


/* timer_handle_t request_timer(short centiseconds)
{
	
} */

void init_timer_driver()
{
	bind_tim_vector();
	init_timer_hw();
}

