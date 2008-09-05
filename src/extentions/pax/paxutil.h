#ifndef PAXUTIL_H
#define PAXUTIL_H

int pax_checkshortlist(int width, PyObject *list,
		       short **parray, int *pnitems);

int pax_checkdoublelist(int width, PyObject *list,
		       double **parray, int *pnitems);
#endif /* PAXUTIL_H */

