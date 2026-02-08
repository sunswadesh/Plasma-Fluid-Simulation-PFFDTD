// Plasma Subroutine (Multi Fluid Model)
// Use with version 1.8.1+

// Author: Jeff Ward
// Last Modified 6/8/05

/*****************************************************************************/
//Defaults
#define ME 9.1066e-31                           // Mass of electron
#define QE -1.6021917e-19                       // Charge of electron
#define AMU 1.6605e-27                          // AMU -> kg
#define K 1.380622e-23                          // Boltzmans Constant

double FREQ_PLASMA = 10e6;			// Plasma Freuicy (Hz)
double FREQ_COL = 0.1;		                // Frequency of collision (% of fp)
double FREQ_CYC = 1.5*FREQ_PLASMA;		// Cyclotron Frequency (Hz)
double ANGLE_E_CYC = 0.0;			// Elevation angle of Cyclotron Frequency (DEGREES)
double ANGLE_A_CYC = 0.0;			// Azimuth angle of Cyclotron Frequency (DEGREES)
double UX_0 = 1.0;				// Average drift velocity (including Neutrals)
double UY_0 = 1.0;
double UZ_0 = 1.0;
double T = 0.0;					// Temparature in Kelvin
double Charge = 1;                              // Delta for charging BC on Antenna (effects electrons only)
#define NS 3                                    // Number of species (NS=1 is only electrons)
double N_0[NS];                                 // initial density of species 
double M[NS];                                   // Array of masses for species
double Q[NS];                                   // Array of charges for species

// Define the mass of the species (0->electron,...) in the PLASMAclear() funtion

double *****UX, *****UY, *****UZ;	        // Partical Movement NOTE: [x][y][z][time][species:0=electron,1+=ions] 1/26/05
double *****N;					// Density (same as UX)
double ***SIG;					// Conductivity (used to define plasma field)
double ***QF;                                   // Charging Factor (for electrons only

void Ninital();
void UBCcalc();
void NBCcalc();

/*****************************************************************************/
/////////////////////////////
// Initialize Arrays for BC /
/////////////////////////////
int PLASMAallocate(int allocate)
{
  int size;
  
  size =  sx*sy*sz*6*sizeof(double) + sy*sz*6*sizeof(double) + sz*6*sizeof(double) + 6*sizeof(double) + sizeof(double);
  UX = darray5(1, sx, 1, sy, 1, sz, 0, 2, 0, NS-1);
  UY = darray5(1, sx, 1, sy, 1, sz, 0, 2, 0, NS-1);
  UZ = darray5(1, sx, 1, sy, 1, sz, 0, 2, 0, NS-1);
  N = darray5(1, sx, 1, sy, 1, sz, 0, 2, 0, NS-1);
  allocate = allocate + 8*size;
  SIG = darray3(1, sx, 1, sy, 1, sz);
  allocate = allocate + 1*size;
  QF = darray3(1, sx, 1, sy, 1, sz);
  allocate = allocate + size;

  // array in routines (AB)
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
 
  for (i=1;i<=sx;i++)
    for (j=1;j<=sy;j++)
      for (k=1;k<=sz;k++)
	  {
	    for (l=0;l<=2;l++)
	    {
		for (m=0;m<NS;m++)
		{
		    UX[i][j][k][l][m] = 0.0;
		    UY[i][j][k][l][m] = 0.0;
		    UZ[i][j][k][l][m] = 0.0;
		    N[i][j][k][l][m] = 0.0;
		}
	      SIG[i][j][k] = 0;
	    }
	    QF[i][j][k] = 1;
	  }
	
  // Turns Plasma On
  for (i=6;i<sx-4;i++)
    for (j=6;j<sy-4;j++)
      for (k=6;k<sz-4;k++)
	if ((ERX[i][j][k]==1) || (ERY[i][j][k]==1) || (ERZ[i][j][k]==1))
	  SIG[i][j][k] = 1.0;

 
}

void PLASMAfree()
{
  freedarray5(UX, 1, sx, 1, sy, 1, sz, 0, 2, 0, 2);
  freedarray5(UY, 1, sx, 1, sy, 1, sz, 0, 2, 0, 2);
  freedarray5(UZ, 1, sx, 1, sy, 1, sz, 0, 2, 0, 2);
  freedarray5(N, 1, sx, 1, sy, 1, sz, 0, 2, 0, 2);
  freedarray3(SIG, 1, sx, 1, sy, 1, sz);
  freedarray3(QF, 1, sx, 1, sy, 1, sz);

}

/*****************************************************************************/
///////////////////////////////////////////////////////////
// Caculate the Average Velocity for the next time sample /
//     Only calculated at points where data is available  /
///////////////////////////////////////////////////////////
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

  for (i=4;i<sx-3;i++)
    for (j=4;j<sy-3;j++)
      for (k=4;k<sz-3;k++)
	for (m=0;m<NS;m++)
	{
	  // Save Old Values
	  UX[i][j][k][0][m] = UX[i][j][k][1][m];
	  UX[i][j][k][1][m] = UX[i][j][k][2][m];
	  UY[i][j][k][0][m] = UY[i][j][k][1][m];
	  UY[i][j][k][1][m] = UY[i][j][k][2][m];
	  UZ[i][j][k][0][m] = UZ[i][j][k][1][m];
	  UZ[i][j][k][1][m] = UZ[i][j][k][2][m];
	  
	  // Calculate averages(using linear techniques set B1=0)
	  ABX = (BX[i][j][k][0] + BX[i][j+1][k][0] + BX[i][j+1][k+1][0] + BX[i][j][k+1][0]
	        + BX[i][j][k][1] + BX[i][j+1][k][1] + BX[i][j+1][k+1][1] + BX[i][j][k+1][1])/8;
	  ABY = (BY[i][j][k][0] + BY[i+1][j][k][0] + BY[i+1][j][k+1][0] + BY[i][j][k+1][0]
	        + BY[i][j][k][1] + BY[i+1][j][k][1] + BY[i+1][j][k+1][1] + BY[i][j][k+1][1])/8;
	  ABZ = (BZ[i][j][k][0] + BZ[i+1][j][k][0] + BZ[i+1][j+1][k][0] + BZ[i][j+1][k][0]
	        + BZ[i][j][k][1] + BZ[i+1][j][k][1] + BZ[i+1][j+1][k][1] + BZ[i][j+1][k][1])/8;

	  // Assuming plasma remains consant at boundary (i.e. delta n = 0) so warm plasma equaitions can be used throughout
	  // Note:NE is at time [2] since density has not been calculated yet
	  // Calculate UX
	  UX[i][j][k][2][m] = UX[i][j][k][0][m] + (QF[i][j][k] * (Q[m]*dt * ( EX[i][j][k][1] + EX[i+1][j][k][1] )
							         + Q[m]*C_U_1 * ( UY[i][j][k][1][m] * BZ_0 + UY_0 * ABZ
										- UZ[i][j][k][1][m] * BY_0 - UZ_0 * ABY
										+ EeX) )
						  - C_U_TX * ( N[i+1][j][k][2][m] - N[i-1][j][k][2][m] ) / N_0[m] ) / M[m]
	                    - C_U_2 * FREQ_COL * FREQ_PLASMA * ( UX[i][j][k][1][m] - UX_0 );
	  // Calculate UY
	  UY[i][j][k][2][m] = UY[i][j][k][0][m] + (QF[i][j][k] * (Q[m]*dt * ( EY[i][j][k][1] + EY[i][j+1][k][1] )
								 + Q[m]*C_U_1 * ( UZ[i][j][k][1][m] * BX_0 + UZ_0 * ABX
										- UX[i][j][k][1][m] * BZ_0 - UX_0 * ABZ
								                + EeY) )
						  - C_U_TY * ( N[i][j+1][k][2][m] - N[i][j-1][k][2][m] ) / N_0[m] ) / M[m]
	                    - C_U_2 * FREQ_COL * FREQ_PLASMA * ( UY[i][j][k][1][m] - UY_0 );
	  // Calculate UZ
	  UZ[i][j][k][2][m] = UZ[i][j][k][0][m] + (QF[i][j][k] * (Q[m]*dt * ( EZ[i][j][k][1] + EZ[i][j][k+1][1] )
								 + Q[m]*C_U_1 * ( UX[i][j][k][1][m] * BY_0 + UX_0 * ABY
										- UY[i][j][k][1][m] * BX_0 - UY_0 * ABX
										+ EeZ ) )
						  - C_U_TZ * ( N[i][j][k+1][2][m] - N[i][j][k-1][2][m] ) / N_0[m] ) / M[m]
	                    - C_U_2 * FREQ_COL * FREQ_PLASMA * ( UZ[i][j][k][1][m] - UZ_0 );
	}


}

/*****************************************************************************/
///////////////////////////////////////////////////
// Calculate the density for the next time sample /
///////////////////////////////////////////////////
void Ncalc()
{
  int i, j, k, m;
  double C_N_tx = dt/dx;
  double C_N_ty = dt/dy;
  double C_N_tz = dt/dz;
	
  for (i=5;i<sx-4;i++)
    for (j=5;j<sy-4;j++)
      for(k=5;k<sz-4;k++)
	  for(m=0;m<NS;m++)
	  {
	      // Save Old Values
	      N[i][j][k][0][m] = N[i][j][k][1][m];
	      N[i][j][k][1][m] = N[i][j][k][2][m];

	      // Calculate Body (Expanded 1st order terms)
	      // Note: the Time difference in the density (last half of the equation) is due to the fact that the cells
	      // "ahead" of the current calculation have not been updated in time
	      N[i][j][k][2][m] = N[i][j][k][0][m] - ( N_0[m] * ( ( UX[i+1][j][k][1][m] - UX[i-1][j][k][1][m] ) * C_N_tx
								 + ( UY[i][j+1][k][1][m] - UY[i][j-1][k][1][m] ) * C_N_ty
								 + ( UZ[i][j][k+1][1][m] - UZ[i][j][k-1][1][m] ) * C_N_tz )
						      + UX_0 * ( N[i+1][j][k][1][m] - N[i-1][j][k][1][m] ) * C_N_tx
						      + UY_0 * ( N[i][j+1][k][1][m] - N[i][j-1][k][1][m] ) * C_N_ty
						      + UZ_0 * ( N[i][j][k+1][1][m] - N[i][j][k-1][1][m] ) * C_N_tz );
	      
	}
}

/*****************************************************************************/
/////////////////////////////////////////////////
// Calculatest the Eletric Field at every point /
// Calculated at every possible point (MODIFIED)/
/////////////////////////////////////////////////
void Ecalcmod()
{
  int i, j, k, m;
  double C_dx = dt/(MU_0*EPSILON_0*dx);
  double C_dy = dt/(MU_0*EPSILON_0*dy);
  double C_dz = dt/(MU_0*EPSILON_0*dz);
  double C_MU = dt/(2*EPSILON_0);
  double JX, JY, JZ;

  for (i=2;i<sx;i++)
    for (j=2;j<sy;j++)
      for (k=2;k<sz;k++)
	{
	  // Save old E
	  EX[i][j][k][0] = EX[i][j][k][1];
	  EY[i][j][k][0] = EY[i][j][k][1];
	  EZ[i][j][k][0] = EZ[i][j][k][1];

	  // Calculate current from plasma
	  JX = 0.0;
	  JY = 0.0;
	  JZ = 0.0;
	  for (m=0;m<NS;m++)
	  {
	      JX = JX + Q[m] * ( N_0[m] * (UX[i][j][k][2][m] + UX[i-1][j][k][2][m]) +  UX_0 * ( N[i][j][k][2][m] + N[i-1][j][k][2][m]) + 2 * N_0[m] * UX_0 );
	      JY = JY + Q[m] * ( N_0[m] * (UY[i][j][k][2][m] + UY[i][j-1][k][2][m]) +  UY_0 * ( N[i][j][k][2][m] + N[i][j-1][k][2][m]) + 2 * N_0[m] * UY_0 );
	      JZ = JZ + Q[m] * ( N_0[m] * (UZ[i][j][k][2][m] + UZ[i][j][k-1][2][m]) +  UZ_0 * ( N[i][j][k][2][m] + N[i][j][k-1][2][m]) + 2 * N_0[m] * UZ_0 );
	  }


	  // Calculate the body
	  // Calculate Ex
	  EX[i][j][k][1] = EX[i][j][k][0] + ( ( BZ[i][j+1][k][1] - BZ[i][j][k][1] ) * C_dy
					    - ( BY[i][j][k+1][1] - BY[i][j][k][1] ) * C_dz
					    - C_MU * SIG[i][j][k] * JX ) * ERX[i][j][k];
		
	  // Calculate Ey
	  EY[i][j][k][1] = EY[i][j][k][0] + ( ( BX[i][j][k+1][1] - BX[i][j][k][1] ) * C_dz
					    - ( BZ[i+1][j][k][1] - BZ[i][j][k][1] ) * C_dx
					    - C_MU * SIG[i][j][k] * JY ) * ERY[i][j][k];
		
	  // Calculate Ez
	  EZ[i][j][k][1] = EZ[i][j][k][0] + ( ( BY[i+1][j][k][1] - BY[i][j][k][1] ) * C_dx
					    - ( BX[i][j+1][k][1] - BX[i][j][k][1] ) * C_dy
					    - C_MU * SIG[i][j][k] * JZ ) * ERZ[i][j][k];
	}
}

/*****************************************************************************/
////////////////////////////////
// Calculate Routine for Plasma /
////////////////////////////////
void Pcalc()
{
  // U
  Ucalc();
  UBCcalc();
  // N
  Ncalc();
  NBCcalc();
}
