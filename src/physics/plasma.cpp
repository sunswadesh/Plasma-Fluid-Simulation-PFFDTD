#include "plasma.h"
#include <omp.h>
#include <stdio.h>
#include <math.h>
#include "../utils/constants.h"
#include "../utils/memallocate.h"

// Variable Definitions
double FREQ_PLASMA = 5.3e6;			// Plasma Frequency (Hz)
double FREQ_COL = 0.27;		                // Frequency of collision (% of fp)
double FREQ_CYC = 18.7;		                // Cyclotron Frequency (Hz)
double ANGLE_E_CYC = 0.0;			// Elevation angle of Cyclotron Frequency (DEGREES)
double ANGLE_A_CYC = 0.0;			// Azimuth angle of Cyclotron Frequency (DEGREES)
double UX_0 = 1.0;				// Average drift velocity (including Neutrals)
double UY_0 = 1.0;
double UZ_0 = 1.0;
double T = 0.0;					// Temparature in Kelvin
double Charge = 1;                              // Delta for charging BC on Antenna (effects electrons only)

double N_0[NS];                                 // initial density of species 
double M[NS];                                   // Array of masses for species
double Q[NS];                                   // Array of charges for species

double *UX, *UY, *UZ;	        // Partical Movement (Flat 1D)
double *N;					// Density (Flat 1D)
double *SIG;					// Conductivity (Flat 1D)
double *QF;                                   // Charging Factor (Flat 1D)

// Externs for Field Arrays (defined in pffdtd.cpp or field modules, declared in plasma.h used here)
// They are included via plasma.h

int PLASMAallocate(int allocate)
{
  int total_grid = (sx+1)*(sy+1)*(sz+1);
  int total_5d = total_grid * 3 * NS;
  
  UX = darray1(0, total_5d);
  UY = darray1(0, total_5d);
  UZ = darray1(0, total_5d);
  N = darray1(0, total_5d);
  allocate = allocate + 4 * total_5d * sizeof(double);
  
  SIG = darray1(0, total_grid);
  allocate = allocate + total_grid * sizeof(double);
  QF = darray1(0, total_grid);
  allocate = allocate + total_grid * sizeof(double);

  // array in routines (AB) - Legacy? Kept for consistency if needed by forgotten routines?
  // The original code calculated allocate but didn't actually allocate AB arrays here? 
  // It said "// array in routines (AB) allocate = ...". 
  // But those AB variables are local to Ucalc loop.
  // So we just ignore it or keep the calculation.
  allocate = allocate+3*(sx-2)*(sy-2)*(sz-2)*sizeof(double);

  return allocate;
}

void PLASMAclear()
{
  int i, j, k, l, m;
  double pop[NS];                       // Population distribution

  // Ion mass (H=1.6727e-27, N=2.3257e-26, O=2.6566e-26, N2=4.6515e-26, NO=4.9824e-26, O2=5.3133e-26)
  // either enter actual weight or use AMU and atomic number to have program i.e. [ME 12*AMU-ME ...]
 
  M[0] = ME;                            // Masses (first must be electrons)
  Q[0] = QE;                            // Charges (first must be electrons)
  pop[0] = 1;                           // Population distribution (electrons = 1, sum of ions should equal electrons)
  M[1] = 2.6566e-26;
  Q[1] = -QE;
  pop[1] = 0.75;
  M[2] = 4.9824e-26;
  Q[2] = -QE;
  pop[2] = 0.25;

  N_0[0] = 4*PI*PI*FREQ_PLASMA*FREQ_PLASMA*ME*EPSILON_0/QE/QE;
  if (NS > 0)
      for (m=1;m<NS;m++)
	  N_0[m] = N_0[0]*pop[m];
 
  // Initialize Arrays to 0
  int total_grid = (sx+1)*(sy+1)*(sz+1);
  int total_5d = total_grid * 3 * NS;
  
  for(int idx = 0; idx < total_5d; idx++) {
      UX[idx] = 0.0;
      UY[idx] = 0.0;
      UZ[idx] = 0.0;
      N[idx] = 0.0;
  }
  for(int idx = 0; idx < total_grid; idx++) {
      SIG[idx] = 0.0;
      QF[idx] = 1.0;
  }

  // Turns Plasma On
  for (i=6;i<sx-4;i++)
    for (j=6;j<sy-4;j++)
      for (k=6;k<sz-4;k++)
	if ((ERX[IDX3(i,j,k)]==1) || (ERY[IDX3(i,j,k)]==1) || (ERZ[IDX3(i,j,k)]==1))
	  SIG[IDX3(i,j,k)] = 1.0;

 
}

void PLASMAfree()
{
   int total_grid = (sx+1)*(sy+1)*(sz+1);
   int total_5d = total_grid * 3 * NS;
   freedarray1(UX, 0, total_5d);
   freedarray1(UY, 0, total_5d);
   freedarray1(UZ, 0, total_5d);
   freedarray1(N, 0, total_5d);
   freedarray1(SIG, 0, total_grid);
   freedarray1(QF, 0, total_grid);
}

void Ucalc()
{
  int i, j, k, m;
  double C_U_1 = 2*dt;
  double C_U_2 = 4*PI*dt;
  double C_U_TX = K*T*dt/dx;
  double C_U_TY = K*T*dt/dy;
  double C_U_TZ = K*T*dt/dz;
  double BX_0 = FREQ_CYC*2*PI*ME/QE*sin(ANGLE_E_CYC*PI/180)*cos(ANGLE_A_CYC*PI/180);
  double BY_0 = FREQ_CYC*2*PI*ME/QE*sin(ANGLE_E_CYC*PI/180)*sin(ANGLE_A_CYC*PI/180);
  double BZ_0 = FREQ_CYC*2*PI*ME/QE*cos(ANGLE_E_CYC*PI/180);
  double ABX, ABY, ABZ;
  double EeX = UY_0 * BZ_0 - UZ_0 * BZ_0; //Effective E field (DC -> UxB)
  double EeY = UZ_0 * BX_0 - UX_0 * BZ_0;
  double EeZ = UX_0 * BY_0 - UY_0 * BX_0;

  #pragma omp parallel for private(j,k,m,ABX,ABY,ABZ,EeX,EeY,EeZ)
  for (i=4;i<sx-3;i++)
    for (j=4;j<sy-3;j++)
      for (k=4;k<sz-3;k++)
	for (m=0;m<NS;m++)
	{
	  // Save Old Values
	  UX[IDX5(i,j,k,0,m)] = UX[IDX5(i,j,k,1,m)];
	  UX[IDX5(i,j,k,1,m)] = UX[IDX5(i,j,k,2,m)];
	  UY[IDX5(i,j,k,0,m)] = UY[IDX5(i,j,k,1,m)];
	  UY[IDX5(i,j,k,1,m)] = UY[IDX5(i,j,k,2,m)];
	  UZ[IDX5(i,j,k,0,m)] = UZ[IDX5(i,j,k,1,m)];
	  UZ[IDX5(i,j,k,1,m)] = UZ[IDX5(i,j,k,2,m)];
	  
	  // Calculate averages(using linear techniques set B1=0)
	  ABX = (BX[IDX4(i,j,k,0)] + BX[IDX4(i,j+1,k,0)] + BX[IDX4(i,j+1,k+1,0)] + BX[IDX4(i,j,k+1,0)]
	        + BX[IDX4(i,j,k,1)] + BX[IDX4(i,j+1,k,1)] + BX[IDX4(i,j+1,k+1,1)] + BX[IDX4(i,j,k+1,1)])/8;
	  ABY = (BY[IDX4(i,j,k,0)] + BY[IDX4(i+1,j,k,0)] + BY[IDX4(i+1,j,k+1,0)] + BY[IDX4(i,j,k+1,0)]
	        + BY[IDX4(i,j,k,1)] + BY[IDX4(i+1,j,k,1)] + BY[IDX4(i+1,j,k+1,1)] + BY[IDX4(i,j,k+1,1)])/8;
	  ABZ = (BZ[IDX4(i,j,k,0)] + BZ[IDX4(i+1,j,k,0)] + BZ[IDX4(i+1,j+1,k,0)] + BZ[IDX4(i,j+1,k,0)]
	        + BZ[IDX4(i,j,k,1)] + BZ[IDX4(i+1,j,k,1)] + BZ[IDX4(i+1,j+1,k,1)] + BZ[IDX4(i,j+1,k,1)])/8;

	  // Assuming plasma remains consant at boundary (i.e. delta n = 0) so warm plasma equaitions can be used throughout
	  // Note:NE is at time [2] since density has not been calculated yet
	  // Calculate UX
	  UX[IDX5(i,j,k,2,m)] = UX[IDX5(i,j,k,0,m)] + (QF[IDX3(i,j,k)] * (Q[m]*dt * ( EX[IDX4(i,j,k,1)] + EX[IDX4(i+1,j,k,1)] )
							         + Q[m]*C_U_1 * ( UY[IDX5(i,j,k,1,m)] * BZ_0 + UY_0 * ABZ
										- UZ[IDX5(i,j,k,1,m)] * BY_0 - UZ_0 * ABY
										+ EeX) )
						  - C_U_TX * ( N[IDX5(i+1,j,k,2,m)] - N[IDX5(i-1,j,k,2,m)] ) / N_0[m] ) / M[m]
	                    - C_U_2 * FREQ_COL * FREQ_PLASMA * ( UX[IDX5(i,j,k,1,m)] - UX_0 );
	  // Calculate UY
	  UY[IDX5(i,j,k,2,m)] = UY[IDX5(i,j,k,0,m)] + (QF[IDX3(i,j,k)] * (Q[m]*dt * ( EY[IDX4(i,j,k,1)] + EY[IDX4(i,j+1,k,1)] )
								 + Q[m]*C_U_1 * ( UZ[IDX5(i,j,k,1,m)] * BX_0 + UZ_0 * ABX
										- UX[IDX5(i,j,k,1,m)] * BZ_0 - UX_0 * ABZ
								                + EeY) )
						  - C_U_TY * ( N[IDX5(i,j+1,k,2,m)] - N[IDX5(i,j-1,k,2,m)] ) / N_0[m] ) / M[m]
	                    - C_U_2 * FREQ_COL * FREQ_PLASMA * ( UY[IDX5(i,j,k,1,m)] - UY_0 );
	  // Calculate UZ
	  UZ[IDX5(i,j,k,2,m)] = UZ[IDX5(i,j,k,0,m)] + (QF[IDX3(i,j,k)] * (Q[m]*dt * ( EZ[IDX4(i,j,k,1)] + EZ[IDX4(i,j,k+1,1)] )
								 + Q[m]*C_U_1 * ( UX[IDX5(i,j,k,1,m)] * BY_0 + UX_0 * ABY
										- UY[IDX5(i,j,k,1,m)] * BX_0 - UY_0 * ABX
										+ EeZ ) )
						  - C_U_TZ * ( N[IDX5(i,j,k+1,2,m)] - N[IDX5(i,j,k-1,2,m)] ) / N_0[m] ) / M[m]
	                    - C_U_2 * FREQ_COL * FREQ_PLASMA * ( UZ[IDX5(i,j,k,1,m)] - UZ_0 );
	}
}

void Ncalc()
{
  int i, j, k, m;
  double C_N_tx = dt/dx;
  double C_N_ty = dt/dy;
  double C_N_tz = dt/dz;
	
  #pragma omp parallel for private(j,k,m)
  for (i=5;i<sx-4;i++)
    for (j=5;j<sy-4;j++)
      for(k=5;k<sz-4;k++)
	  for(m=0;m<NS;m++)
	  {
	      // Save Old Values
	      N[IDX5(i,j,k,0,m)] = N[IDX5(i,j,k,1,m)];
	      N[IDX5(i,j,k,1,m)] = N[IDX5(i,j,k,2,m)];

	      // Calculate Body (Expanded 1st order terms)
	      // Note: the Time difference in the density (last half of the equation) is due to the fact that the cells
	      // "ahead" of the current calculation have not been updated in time
	      N[IDX5(i,j,k,2,m)] = N[IDX5(i,j,k,0,m)] - ( N_0[m] * ( ( UX[IDX5(i+1,j,k,1,m)] - UX[IDX5(i-1,j,k,1,m)] ) * C_N_tx
								 + ( UY[IDX5(i,j+1,k,1,m)] - UY[IDX5(i,j-1,k,1,m)] ) * C_N_ty
								 + ( UZ[IDX5(i,j,k+1,1,m)] - UZ[IDX5(i,j,k-1,1,m)] ) * C_N_tz )
						      + UX_0 * ( N[IDX5(i+1,j,k,1,m)] - N[IDX5(i-1,j,k,1,m)] ) * C_N_tx
						      + UY_0 * ( N[IDX5(i,j+1,k,1,m)] - N[IDX5(i,j-1,k,1,m)] ) * C_N_ty
						      + UZ_0 * ( N[IDX5(i,j,k+1,1,m)] - N[IDX5(i,j,k-1,1,m)] ) * C_N_tz );
	      
	}
}

void Ecalcmod()
{
  int i, j, k, m;
  double C_dx = dt/(MU_0*EPSILON_0*dx);
  double C_dy = dt/(MU_0*EPSILON_0*dy);
  double C_dz = dt/(MU_0*EPSILON_0*dz);
  double C_MU = dt/(2*EPSILON_0);
  double JX, JY, JZ;

  #pragma omp parallel for private(j,k,m,JX,JY,JZ)
  for (i=2;i<sx;i++)
    for (j=2;j<sy;j++)
      for (k=2;k<sz;k++)
	{
	  // Save old E
	  EX[IDX4(i,j,k,0)] = EX[IDX4(i,j,k,1)];
	  EY[IDX4(i,j,k,0)] = EY[IDX4(i,j,k,1)];
	  EZ[IDX4(i,j,k,0)] = EZ[IDX4(i,j,k,1)];

	  // Calculate current from plasma
	  JX = 0.0;
	  JY = 0.0;
	  JZ = 0.0;
	  for (m=0;m<NS;m++)
	  {
	      JX = JX + Q[m] * ( N_0[m] * (UX[IDX5(i,j,k,2,m)] + UX[IDX5(i-1,j,k,2,m)]) +  UX_0 * ( N[IDX5(i,j,k,2,m)] + N[IDX5(i-1,j,k,2,m)]) + 2 * N_0[m] * UX_0 );
	      JY = JY + Q[m] * ( N_0[m] * (UY[IDX5(i,j,k,2,m)] + UY[IDX5(i,j-1,k,2,m)]) +  UY_0 * ( N[IDX5(i,j,k,2,m)] + N[IDX5(i,j-1,k,2,m)]) + 2 * N_0[m] * UY_0 );
	      JZ = JZ + Q[m] * ( N_0[m] * (UZ[IDX5(i,j,k,2,m)] + UZ[IDX5(i,j,k-1,2,m)]) +  UZ_0 * ( N[IDX5(i,j,k,2,m)] + N[IDX5(i,j,k-1,2,m)]) + 2 * N_0[m] * UZ_0 );
	  }


	  // Calculate the body
	  // Calculate Ex
	  EX[IDX4(i,j,k,1)] = EX[IDX4(i,j,k,0)] + ( ( BZ[IDX4(i,j+1,k,1)] - BZ[IDX4(i,j,k,1)] ) * C_dy
					    - ( BY[IDX4(i,j,k+1,1)] - BY[IDX4(i,j,k,1)] ) * C_dz
					    - C_MU * SIG[IDX3(i,j,k)] * JX ) * ERX[IDX3(i,j,k)];
		
	  // Calculate Ey
	  EY[IDX4(i,j,k,1)] = EY[IDX4(i,j,k,0)] + ( ( BX[IDX4(i,j,k+1,1)] - BX[IDX4(i,j,k,1)] ) * C_dz
					    - ( BZ[IDX4(i+1,j,k,1)] - BZ[IDX4(i,j,k,1)] ) * C_dx
					    - C_MU * SIG[IDX3(i,j,k)] * JY ) * ERY[IDX3(i,j,k)];
		
	  // Calculate Ez
	  EZ[IDX4(i,j,k,1)] = EZ[IDX4(i,j,k,0)] + ( ( BY[IDX4(i+1,j,k,1)] - BY[IDX4(i,j,k,1)] ) * C_dx
					    - ( BX[IDX4(i,j+1,k,1)] - BX[IDX4(i,j,k,1)] ) * C_dy
					    - C_MU * SIG[IDX3(i,j,k)] * JZ ) * ERZ[IDX3(i,j,k)];
	}
}

void Pcalc()
{
  // U
  Ucalc();
  UBCcalc();
  // N
  Ncalc();
  NBCcalc();
}
