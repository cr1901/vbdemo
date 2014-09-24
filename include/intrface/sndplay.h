#ifndef SNDPLAY_H
#define SNDPLAY_H

#include "intrface/sndtrack.h"

typedef int sound_handle_t;

void snd_init();
void play_music(MUSIC_ID track_no);
void stop_music();
sound_handle_t play_sound(SOUND_ID sound_no);
void stop_sound(sound_handle_t s_ptr);

#endif        /*  #ifndef SNDPLAY_H  */

