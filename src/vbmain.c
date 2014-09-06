#include "init.h"
#include "mainloop.h"

/* There's not much here... */

int main()
{    
    init_vb(); /* One-time init, including objects which are loaded once. */
    main_loop();
    jump_to_reset();
    return 0; /* Very bad things (TM) happen if we get here... */
}
