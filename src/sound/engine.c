/* The sound engine main procedure. The sound engine is interrupt driven. If
the game wants a sound to play, it makes a request. A request can be music (loop
a sequence of register changes), a single sound, or a sequence of sounds to be
played once. The sound engine will return a pointer to data which can be used
to check if sound is still playing or done playing. Sounds/music can be cancelled
at anytime by requesting the sound driver via the saved handle. Likewise, sounds
can be replaced by requesting the sound driver in the same manner.

The sound driver keeps a variable which detects if another timer interrupt was received
since processing began. If so, the engine finishes the current frame, lets the 
second interrupt be serviced, and then updates already playing sounds but ignores
managing new/replaced sounds. */

/* Sound channel allocation:
1-3: Music only
4: Music/sound. Each request overrides the previous
5: Music/sound. Lockable, so that music/sound will not be interrupted.
6: Sound only. Who wants to listen to noise for music? */
