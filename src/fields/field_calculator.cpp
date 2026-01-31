#include "field_calculator.h"
#include <math.h>

// Global variables from pffdtd.cpp (Externs)
extern double dt, dx, dy, dz;
extern int sx, sy, sz;
extern double ****EX, ****EY, ****EZ;
extern double ****BX, ****BY, ****BZ;
extern double ***ERX, ***ERY, ***ERZ;

void Ecalc()
{
  int i, j, k;
  double C_dx = dt/(MU_0*EPSILON_0*dx);
  double C_dy = dt/(MU_0*EPSILON_0*dy);
  double C_dz = dt/(MU_0*EPSILON_0*dz);


  // Calculate the body (NOTE: One additional cell is added to eliminate the need for seperate loops for Ex, Ey, and EZ)
  // Also ERX is actually 1/Er see setup2
  for (i=2;i<sx;i++)
    for (j=2;j<sy;j++)
      for (k=2;k<sz;k++)
	{
	  // Save Old Values
	  EX[i][j][k][0] = EX[i][j][k][1];
	  EY[i][j][k][0] = EY[i][j][k][1];
	  EZ[i][j][k][0] = EZ[i][j][k][1];

	  // Calculate Ex
 	  EX[i][j][k][1] = EX[i][j][k][0] + ( ( BZ[i][j+1][k][1] - BZ[i][j][k][1] ) * C_dy
					    - ( BY[i][j][k+1][1] - BY[i][j][k][1] ) * C_dz ) * ERX[i][j][k];
 		
	  // Calculate Ey
 	  EY[i][j][k][1] = EY[i][j][k][0] + ( ( BX[i][j][k+1][1] - BX[i][j][k][1] ) * C_dz
					    - ( BZ[i+1][j][k][1] - BZ[i][j][k][1] ) * C_dx ) * ERY[i][j][k];
		
	  // Calculate Ez
 	  EZ[i][j][k][1] = EZ[i][j][k][0] + ( ( BY[i+1][j][k][1] - BY[i][j][k][1] ) * C_dx
					    - ( BX[i][j+1][k][1] - BX[i][j][k][1] ) * C_dy ) * ERZ[i][j][k];
	}

}

void Bcalc()
{
  int i,j,k;
  double C_dx = dt/dx;
  double C_dy = dt/dy;
  double C_dz = dt/dz;

  // Calculate the body
  for (i=2;i<sx;i++)
    for (j=2;j<sy;j++)
      for (k=2;k<sz;k++)
	{
	  // Save Old Values
	  BX[i][j][k][0] = BX[i][j][k][1];
	  BY[i][j][k][0] = BY[i][j][k][1];
	  BZ[i][j][k][0] = BZ[i][j][k][1];

	  // Calculate Bx
	  BX[i][j][k][1] = BX[i][j][k][0] + ( ( EY[i][j][k][1] - EY[i][j][k-1][1] ) * C_dz
				          - ( EZ[i][j][k][1] - EZ[i][j-1][k][1] ) * C_dy );
	  // Calculate By
	  BY[i][j][k][1] = BY[i][j][k][0] + ( ( EZ[i][j][k][1] - EZ[i-1][j][k][1] ) * C_dx
				          - ( EX[i][j][k][1] - EX[i][j][k-1][1] ) * C_dz );
	  // Calculate Bz
	  BZ[i][j][k][1] = BZ[i][j][k][0] + ( ( EX[i][j][k][1] - EX[i][j-1][k][1] ) * C_dy
				          - ( EY[i][j][k][1] - EY[i-1][j][k][1] ) * C_dx );
	}
}
