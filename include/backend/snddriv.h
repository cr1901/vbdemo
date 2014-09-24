#ifndef SNDDRIV_H
#define SNDDRIV_H

#include "backend/snddata.h"

void write_instrument(int channel_no, INSTRUMENT inst);
void write_note(int channel_no, NOTE note);
#endif        /*  #ifndef SNDDRIV_H  */

