#include "file_handler.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "../utils/constants.h"
#include "../utils/memallocate.h" // For darray/iarray/EMBCallocate etc
#include "output.h" // For headvc, headfd
#include "../physics/plasma.h" // For plasma globals if needed in setup2/ClearArrays

// Extern globals from pffdtd.cpp
extern int sx, sy, sz;
extern double dx, dy, dz, dt, df;
extern int FAIL_SAFE, PLASMA_CYCLE;
extern int Snum;
extern int **Sloc;
extern double *Spar;
extern int plasma;
extern int fields;
extern int frate;
extern int fout[6];
extern int floc[2][3];
extern double ****EX, ****EY, ****EZ;
extern double ****BX, ****BY, ****BZ;
extern double ***ERX, ***ERY, ***ERZ;
extern double *VOLT, *CURRENT;
extern double ***QF, ***SIG; // From plasma?
extern double Charge;
// Need constants C, MU_0, EPSILON_0?

// Forward declarations if not in headers
extern int EMBCallocate(int);
extern void EMBCclear();
extern void EMBCfree();
// PLASMAallocate is in plasma.h which is included

FILE *openfile(char filepre[81], char filesuf[3])
{
  char temp[81];
  FILE *filevar;
  
  // Open Source File
  strcpy(temp, filepre);
  strcat(temp, filesuf);
  if ((filevar = fopen(temp,"w")) == NULL)
    {
      printf("Error opening file: %s\n", temp);
      exit(1);
    }
  return filevar;
}

FILE *openfile2(char filepre[81], char filesuf[3])
{
  char temp[81];
  FILE *filevar;
  
  // Open Source File
  strcpy(temp, filepre);
  strcat(temp, filesuf);
  if ((filevar = fopen(temp,"r")) == NULL)
    {
      printf("Error opening file: %s\n", temp);
      exit(1);
    }
  return filevar;
}

int setup1(FILE *fp1)
{
  char tp1[80];
  char tp2[10],tp3[10],tp4[10];
 
  // File Name
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  printf("\t%s",tp1);
  // Grid Parameters
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  printf("\t%s",tp1);
  fgets(tp1,80,fp1);
  if (sscanf(tp1,"%d\t%d\t%d",&sx,&sy,&sz)!=3)
    return 1;
  printf("\tsx=%d   \tsy=%d   \tsz=%d\n",sx,sy,sz);
  fgets(tp1,80,fp1);
  if (sscanf(tp1,"%s\t%s\t%s",tp2,tp3,tp4)!=3)
    return 1;
  dx=atof(tp2);
  dy=atof(tp3);
  dz=atof(tp4);
  printf("\tdx=%5.3f\tdy=%5.3f\tdz=%5.3f\n",dx,dy,dz);
  dt=dx/(2*C);                         // Time iteration
  printf("\tdt = %e\n",dt);
  // Fail Safe Parameters
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  printf("\t%s",tp1);
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  FAIL_SAFE = atoi(tp1);
  printf("\tMax Iteration = %d",FAIL_SAFE);
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  PLASMA_CYCLE = atoi(tp1);
  printf("\tMax Plasma Cycles = %d\n",PLASMA_CYCLE);
  // Source Parameters
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  printf("\t%s",tp1);
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  Snum = atoi(tp1);

  return 0;
}

int setup2(FILE *fp1)
{
  char tp1[80];
  char tp2[10];
  int a,b;
  int i,j,k,l,m,n;
  double ER[2];

  // Source Parameters part 2
  for (a=1;a<=Snum;a++)
    {
      fgets(tp1,80,fp1);
      if (sscanf(tp1,"%d\t%d\t%d\t%d\t%d\t%s",&Sloc[a][0],&Sloc[a][1],&Sloc[a][2],&Sloc[a][3],&Sloc[a][4],tp2)!=6)
	return 1;
      Spar[a] = atof(tp2);
      if ( (a==1) | (a==Snum) )
	printf("\t#%d (%d,%d,%d) Field->%d Type->%d Parameter->%5.3f\n",a,Sloc[a][0],Sloc[a][1],Sloc[a][2],Sloc[a][3],Sloc[a][4],Spar[a]);
      if ( (a==2) & (a!=Snum) )
	printf("\t\t.\n\t\t.\n\t\t.\n");
    }
  // Dielectric Parameters
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  printf("\t%s",tp1);
   if (fgets(tp1,80,fp1)==NULL)
    return 1;
  ER[0] = atof(tp1);
  printf("\tEr 1 = %5.3f\n",ER[0]);
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  ER[1] = atof(tp1);
  printf("\tEr 2 = %5.3f\n",ER[1]);
  // Antenna Parameters
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  printf("\t%s",tp1);
  if (fgets(tp1,80,fp1)==NULL)
    return 1;
  b = atoi(tp1);
  for (a=1;a<=b;a++)
    {
      fgets(tp1,80,fp1);
      if (sscanf(tp1,"%d\t%d\t%d\t%d\t%d\t%d",&i,&j,&k,&l,&m,&n)!=6)
	return 1;
      switch (l)
	{
	case 1:
          ERX[i][j][k] = 0;
	  if (plasma == 1)
	      QF[i][j][k] = Charge;
          break;
        case 2:
	  ERX[i][j][k] = 1/ER[0];
	  break;
        case 3:
	  ERX[i][j][k] = 1/ER[1];
          break;
        default:
	  ERX[i][j][k] = 1;
	  break;
	}
      switch (m)
	{
	case 1:
          ERY[i][j][k] = 0;
	  if (plasma == 1)
	      QF[i][j][k] = Charge;
          break;
        case 2:
	  ERY[i][j][k] = 1/ER[0];
	  break;
        case 3:
	  ERY[i][j][k] = 1/ER[1];
          break;
        default:
	  ERY[i][j][k] = 1;
	  break;
	}
      switch (n)
	{
	case 1:
          ERZ[i][j][k] = 0;
	  if (plasma == 1)
	      QF[i][j][k] = Charge;
          break;
        case 2:
	  ERZ[i][j][k] = 1/ER[0];
	  break;
        case 3:
	  ERZ[i][j][k] = 1/ER[1];
          break;
        default:
	  ERZ[i][j][k] = 1;
	  break;
	}
      if ((plasma ==1) & (l>1) & (m>1) & (n>1))
	SIG[i][j][k] = 0;                             // Turns off Plasma inside dielectrics
      if ( (a==1) | (a==b) )
	printf("\t(%d,%d,%d) 1/Erx->%5.3f 1/Ery->%5.3f 1/Erz->%5.3f \n",i,j,k,ERX[i][j][k],ERY[i][j][k],ERZ[i][j][k]);
      if ( (a==2) & (a!=b) )
	printf("\t\t.\n\t\t.\n\t\t.\n");

    }
  // Points of Field output (opt.)
  if (fgets(tp1,80,fp1)==NULL)
    return 0;
  fields = 1;                                         // Turns field output on
  printf("\t%s",tp1);
  fgets(tp1,80,fp1);
  if (sscanf(tp1,"%d\t%d\t%d\t%d\t%d\t%d\t%d",&frate,&fout[0],&fout[1],&fout[2],&fout[3],&fout[4],&fout[5])<2)
    return 1;
  printf("\tOutput ->");
  if (fout[0]==1)
    printf(" Electric");
  if (fout[1]==1)
    printf(" Magnetic");
  if (fout[2]==1)
    printf(" eVelocity");
  if (fout[3]==1)
    printf(" eDensity");
  if (fout[4]==1)
    printf(" ionVelocity");
  if (fout[5]==1)
    printf(" ionDensity");
  printf("\n");
  fgets(tp1,80,fp1);
  if (sscanf(tp1,"%d\t%d\t%d",&floc[0][0],&floc[0][1],&floc[0][2])!=3)
    return 1;
  printf("\tLower Limit [%d %d %d]\n",floc[0][0],floc[0][1],floc[0][2]);
  fgets(tp1,80,fp1);
  if (sscanf(tp1,"%d\t%d\t%d",&floc[1][0],&floc[1][1],&floc[1][2])!=3)
    return 1;
  printf("\tUpper Limit [%d %d %d]\n",floc[1][0],floc[1][1],floc[1][2]);
  
  return 0;
}

void ClearArrays()
{
  int i, j, k, l;

  for (i=1;i<=sx;i++)
    for (j=1;j<=sy;j++)
      for (k=1;k<=sz;k++)
	{
	  for (l=0;l<=1;l++)
	    {
	      EX[i][j][k][l] = 0;
	      EY[i][j][k][l] = 0;
	      EZ[i][j][k][l] = 0;
	      BX[i][j][k][l] = 0;
	      BY[i][j][k][l] = 0;
	      BZ[i][j][k][l] = 0;
	    }
	  ERX[i][j][k] = 1;
	  ERY[i][j][k] = 1;
	  ERZ[i][j][k] = 1;
	}

  for (j=1;j<=Snum;j++)
  {
      VOLT[j] = 0;
      CURRENT[j] = 0;
  }
}
