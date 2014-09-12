#include "init.h"
#include "mainloop.h"

/* There's not much here... */

int main()
{    
    init_vb(); /* One-time init, including objects which are loaded once. */
    main_loop(); /* Game processing. We should never return, but if we do... */
    jump_to_reset(); /* Reset the console from the very beginning. */
    return 0; /* Very bad things (TM) happen if we get here... */
}
