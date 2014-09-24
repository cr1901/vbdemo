#ifndef SNDDATA_H
#define SNDDATA_H

typedef signed char waveform[32];
typedef signed char envelope[32];

typedef struct instrument
{
	waveform * wavedata;
	envelope * env_data;
}INSTRUMENT;

typedef struct note
{
	unsigned short frequency; /* In Hz. */
	/* 	unsigned short volume; */ /* In... units :P. */
	unsigned short duration; /* In centiseconds. */
}NOTE;

typedef struct figure
{
	unsigned char num_notes;
	NOTE * notes;
}FIGURE;


#endif        /*  #ifndef SNDDATA_H  */

