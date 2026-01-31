#include "source.h"
#include <stdio.h> // For printf if needed

// Access to global variables defined in pffdtd.cpp
// In a full modularization, these should be passed as arguments or part of a class.
// For Phase 2, we use extern to link to them.

extern int **Sloc;
extern double *Spar;
extern double dt, dx, dy, dz, df;
extern double ****EX, ****EY, ****EZ;
extern double ****BX, ****BY, ****BZ;
extern double *VOLT, *CURRENT;

void Esource(double timev, int a)
{
  double value;
  double sd, delay, peak, temp, offset, gain;
  
  // Sine
  if (Sloc[a][4] == 1)
    value = 5*sin(2 * PI * Spar[a] * timev) - 0.0;
  
  // Pulse
  if (Sloc[a][4] == 2)
    {
      if ( (timev*Spar[a]/4) < 1 )
	value = -1;
      else
	value = 0;
    }
  
  // Rased Cosine Wave
  if (Sloc[a][4] == 3)
    {
      if ( (timev*Spar[a]/4) < 1 )
	value = 0.5 * cos(2 * PI * Spar[a] * timev) - 0.5;
      else
	value = 0;
    }

  //Gause
  if (Sloc[a][4] == 4)
    {
      sd = Spar[a];
      delay = sd * 5;
      temp = (delay * dt - timev) / (sd * dt);
      value = -1e-7 / (sd * dt) * exp(-0.5 * temp * temp);
    }
	
  //D Gause
  if (Sloc[a][4] == 5)
    {
	sd = 0.25/Spar[a];  // Sets standard deveation to about 1/4 of desired peak frequency Notes: must be > 2*dt, and < MAXITERATION / 10
      delay = 5 * sd;
      temp = (timev-delay)/(sd*sd*sd*2.50662827463)*exp(-(timev-delay)*(timev-delay)/(2*sd*sd));
      peak = 0.241970724519/(sd*sd);
      value = temp/peak;
//      printf("%f,%f, %f, %f, %f, %f",Spar[a],sd*1e7,delay*1e7,temp,peak,value);
     
   }

  //DC
  if (Sloc[a][4] == 6)
      value = Spar[a];
 
  //Sinc
  if (Sloc[a][4] == 7)
  {
      offset = 10 / df * dt + dt/2; // center of pulse is at # plasma cycles, dt/2 is added to avoid div by zero
      gain = 2 * Spar[a] * dt; // set power spectral density equal to one
      temp = Spar[a] * (timev - offset) * 2 * PI;
      value = sin (temp) / temp * gain;
  }

  // orentation of source
  if (Sloc[a][3] == 1)
    EX[Sloc[a][0]][Sloc[a][1]][Sloc[a][2]][1] = value / dx;
  if (Sloc[a][3] == 2)
    EY[Sloc[a][0]][Sloc[a][1]][Sloc[a][2]][1] = value / dy;
  if (Sloc[a][3] == 3)
    EZ[Sloc[a][0]][Sloc[a][1]][Sloc[a][2]][1] = value / dz;

}

void Rcalc( int a)
{
  int x, y, z;
		
  // location of source
  x = Sloc[a][0];
  y = Sloc[a][1];
  z = Sloc[a][2];
	
  if (Sloc[a][3] == 1)
    {
      CURRENT[a] = ( ( BY[x][y][z][1] - BY[x][y][z+1][1] ) * dx
		    + ( BZ[x][y+1][z][1] - BZ[x][y][z][1] ) * dy ) / MU_0;
      // ASSUMING THE CURRENT / VOLTAGE VARIES SLOWLY COMPARD TO dt
      VOLT[a] = - EX[x][y][z][1] * dx;
    }
  if (Sloc[a][3] == 2)
    {
      CURRENT[a] = ( ( BX[x][y][z+1][1] - BX[x][y][z][1] ) * dx
		    + ( BZ[x][y][z][1] - BZ[x+1][y][z][1] ) * dy ) / MU_0;
      // ASSUMING THE CURRENT / VOLTAGE VARIES SLOWLY COMPARD TO dt
      VOLT[a] = - EY[x][y][z][1] * dy;
    }
  if (Sloc[a][3] == 3)
    {
      CURRENT[a] = ( ( BX[x][y][z][1] - BX[x][y+1][z][1] ) * dx
		    + ( BY[x+1][y][z][1] - BY[x][y][z][1] ) * dy ) / MU_0;
      // ASSUMING THE CURRENT / VOLTAGE VARIES SLOWLY COMPARD TO dt
      VOLT[a] = - EZ[x][y][z][1] * dz;
    }

}
