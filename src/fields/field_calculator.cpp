#include "field_calculator.h"
#include <math.h>
#include <omp.h>
#include <stdio.h>
#include "../utils/constants.h"

// Time-level rotation indices (declared extern in constants.h).
// The "save old values" copies are gone: each kernel reads the *_old level,
// writes the *_cur level, then swaps the pair once per step.
int tlE_old = 0, tlE_cur = 1, tlB_old = 0, tlB_cur = 1;

// Global variables from pffdtd.cpp (Externs)
extern double dt, dx, dy, dz;
extern int sx, sy, sz;
extern double *EX, *EY, *EZ;
extern double *BX, *BY, *BZ;
extern double *ERX, *ERY, *ERZ;

void Ecalc()
{
  int i, j, k;
  double C_dx = dt/(MU_0*EPSILON_0*dx);
  double C_dy = dt/(MU_0*EPSILON_0*dy);
  double C_dz = dt/(MU_0*EPSILON_0*dz);


  // Rotate the E time levels first: *_old is the buffer to read (previous
  // step), *_cur the buffer to write. After the update below, *_cur holds
  // the newest values for the rest of this step (no data copies).
  { int t = tlE_old; tlE_old = tlE_cur; tlE_cur = t; }

  // Calculate the body (NOTE: One additional cell is added to eliminate the need for seperate loops for Ex, Ey, and EZ)
  // Also ERX is actually 1/Er see setup2

  #pragma omp parallel for private(j,k)
  for (i=2;i<sx;i++)
    for (j=2;j<sy;j++)
      for (k=2;k<sz;k++)
	{
	  // Time-level rotation: read the previous (*_old) level, write the
	  // current (*_cur) level. The old per-step "save old values" copies
	  // are eliminated; the pair was rotated once at the top of this
	  // function, so *_cur holds the newest values from here on.

	  // Calculate Ex
 	  EX[IDX4(i,j,k,tlE_cur)] = EX[IDX4(i,j,k,tlE_old)] + ( ( BZ[IDX4(i,j+1,k,tlB_cur)] - BZ[IDX4(i,j,k,tlB_cur)] ) * C_dy
							    - ( BY[IDX4(i,j,k+1,tlB_cur)] - BY[IDX4(i,j,k,tlB_cur)] ) * C_dz ) * ERX[IDX3(i,j,k)];

	  // Calculate Ey
 	  EY[IDX4(i,j,k,tlE_cur)] = EY[IDX4(i,j,k,tlE_old)] + ( ( BX[IDX4(i,j,k+1,tlB_cur)] - BX[IDX4(i,j,k,tlB_cur)] ) * C_dz
							    - ( BZ[IDX4(i+1,j,k,tlB_cur)] - BZ[IDX4(i,j,k,tlB_cur)] ) * C_dx ) * ERY[IDX3(i,j,k)];

	  // Calculate Ez
 	  EZ[IDX4(i,j,k,tlE_cur)] = EZ[IDX4(i,j,k,tlE_old)] + ( ( BY[IDX4(i+1,j,k,tlB_cur)] - BY[IDX4(i,j,k,tlB_cur)] ) * C_dx
							    - ( BX[IDX4(i,j+1,k,tlB_cur)] - BX[IDX4(i,j,k,tlB_cur)] ) * C_dy ) * ERZ[IDX3(i,j,k)];
	}
}

void Bcalc()
{
  int i,j,k;
  double C_dx = dt/dx;
  double C_dy = dt/dy;
  double C_dz = dt/dz;

  // Rotate the B time levels first: *_old is the buffer to read (previous
  // step), *_cur the buffer to write. After the update below, *_cur holds
  // the newest values for the rest of this step (no data copies).
  { int t = tlB_old; tlB_old = tlB_cur; tlB_cur = t; }

  // Calculate the body
  #pragma omp parallel for private(j,k)
  for (i=2;i<sx;i++)
    for (j=2;j<sy;j++)
      for (k=2;k<sz;k++)
	{
	  // Time-level rotation: read the previous (*_old) level, write the
	  // current (*_cur) level. The old per-step "save old values" copies
	  // are eliminated; the pair was rotated once at the top of this
	  // function, so *_cur holds the newest values from here on.

	  // Calculate Bx
	  BX[IDX4(i,j,k,tlB_cur)] = BX[IDX4(i,j,k,tlB_old)] + ( ( EY[IDX4(i,j,k,tlE_cur)] - EY[IDX4(i,j,k-1,tlE_cur)] ) * C_dz
						          - ( EZ[IDX4(i,j,k,tlE_cur)] - EZ[IDX4(i,j-1,k,tlE_cur)] ) * C_dy );
	  // Calculate By
	  BY[IDX4(i,j,k,tlB_cur)] = BY[IDX4(i,j,k,tlB_old)] + ( ( EZ[IDX4(i,j,k,tlE_cur)] - EZ[IDX4(i-1,j,k,tlE_cur)] ) * C_dx
						          - ( EX[IDX4(i,j,k,tlE_cur)] - EX[IDX4(i,j,k-1,tlE_cur)] ) * C_dz );
	  // Calculate Bz
	  BZ[IDX4(i,j,k,tlB_cur)] = BZ[IDX4(i,j,k,tlB_old)] + ( ( EX[IDX4(i,j,k,tlE_cur)] - EX[IDX4(i,j-1,k,tlE_cur)] ) * C_dy
						          - ( EY[IDX4(i,j,k,tlE_cur)] - EY[IDX4(i-1,j,k,tlE_cur)] ) * C_dx );
	}
}
