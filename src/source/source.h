#ifndef SOURCE_H
#define SOURCE_H

#include <math.h>
#include "../utils/constants.h"

// Function Prototypes
extern double *EX, *EY, *EZ;
extern double *BX, *BY, *BZ;
void Esource(double timev, int a);
void Rcalc(int a);

#endif // SOURCE_H
