#include "backend/viddriv.h"
#include "libgccvb/libgccvb.h"

void setup_initial_vip()
{
	vbDisplayOn();
	vbSetColTable();
	vbDisplayHide();
}
