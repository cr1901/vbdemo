#include "backend/viddriv.h"
#include <libgccvb.h>

void setup_initial_vip()
{
	vbDisplayOn();
	vbSetColTable();
	vbDisplayHide();
}
