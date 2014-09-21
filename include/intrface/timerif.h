#ifndef TIMERIF_H
#define TIMERIF_H

typedef int timer_handle_t;
typedef void * tick_count_t;

timer_handle_t request_timer(short centiseconds,  void (*)(volatile void *), volatile void *);
int timer_expired(timer_handle_t t_ptr);
timer_handle_t restart_timer(timer_handle_t t_ptr);
void remove_timer(timer_handle_t t_ptr);
void init_timer_driver();
void stop_timer_driver();

/* int capture_tick(tick_count_t t_ptr);
short difftick(tick_count_t end, tick_count_t begin); */


#endif        /*  #ifndef TIMERIF_H  */

