#include "libgccvb/libgccvb.h"
#include "gamectl.h"

void triangle_mainproc()
{
	WA[31].head = WRLD_END;
	 (* ((short *) 0x0000)) = 0xFFFF;
	 (* ((short *) 0x8000)) = 0xFFFF;
	 (* ((short *) 0x10000)) = 0xFFFF;
	 (* ((short *) 0x18000)) = 0xFFFF;
	 vbDisplayShow();
}
