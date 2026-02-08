//
//  FDTD Code for Hot Magntized Plasma
//
//  Basic FDTD w/ Electrons and Ions
//
#define pffdtdver 1.8
// actual vesion 1.8.2
//
// 1.0 Working program
// 1.1 Two fluids (e, ion)
// 1.2.0 Current term absorbed into maxwells equations (speed / memory) but 2 fluids removed for cold plasma.
// 1.2.1 Can handle labaratory type experiments
// 1.3 Decrease visual output to speed processing.
// 1.4 Modified code to take arguments and import parameter files.
// 1.4.1 Improved exiting procedure. (12/19/02)
// 1.5.0 Errors found in Plasma are corrected.
// 1.6.0 Errors in calculating current have be fixed
// 1.7.0 Two Fluid model added back in
// 1.7.1 DC Sweep is added to test Langmuir Probes (Tempurature effects)
// 1.7.2 Higher Order Terms Removed from Plasma.h (N_1*U_1) in attempt to improve stability
// 1.7.3 Converted source output to every iteration to enable long runs for ion analysis
// 1.7.4 Delta added to plasma charge to set charging BC on antenna (see plasma.h)
// 1.8.0 Added multi species of ions
// 1.8.1 Collision frequency changed to ratio of plasma
// 1.8.2 Fixed problems with sinc source
//
//  Last Modified
#define pffdtdmonth 2
#define pffdtdday 14
#define pffdtdyear 2005
//
// Written for partial completions of Jeffrey D. Ward's Master Thesis
// Purpose: To be used to analyise data from Plasma Frequency Probes
/*****************************************************************************/
// Identified problems
//
// 1. There is a direct relation between stability at max_iteration, density, and grid size.
// 2. Boundary conditions must be improved.
//
/*****************************************************************************/
// Returns / Errors
// 0 - Exited Correctly
// 1 - Error in Opening File
// 2 - Not Enough Memory
// 3 - Error in Input File Format
// 4 - Error in abot subroutine
//
/*****************************************************************************/

// LIBRARIES
#include "math.h"
#include "stdio.h"
#include "string.h"
#include "stddef.h"
#include "stdlib.h"
#include "time.h"
#include "signal.h"
//#include "malloc.h"

// Constants
#define PI 3.14159265359
#define MU_0 1.25663706143591729538505735331180115367886775e-6
#define EPSILON_0 8.85418781762038985053656303171075026060837e-12
#define C 2.998e8

// Variables
// Flags
int Q_flag;				// Flag to quit
int plasma;				// Flags (1 = present, 0 = not present)
int fields;                             // Flags (1 = output fields, 0 = no output)
// Define pointers to field values
double ****EX, ****EY, ****EZ;		// Electric Field
double ****BX, ****BY, ****BZ;		// Magntic Desplacement
double ***ERX, ***ERY, ***ERZ;		// 1/Relitive Pervitvity
// Grid difinitions
int sx, sy, sz;				// Grid Size
double dx, dy, dz, dt, df;		// Grid Spacing
// Source Variables
int Snum;                               // Number of Sources
int **Sloc;				// Location of Source (x,y,z,effected field[x-1,y-2,z-3],type of source)
double *Spar;                           // Source Parameter
// Output Variables
// Used to calculate impedance
double *VOLT, *CURRENT;               // Used to output source conditions
// Used to output fields
int fout[6];                           // Type of fields to be outputed
int frate;                              // Rate at which fields are output (# of iterations/output)
int floc[2][3];                         // Lower/Upper corneres where fields are outputed
// Fail safes (use to stop run away programs)
int FAIL_SAFE;				// Max Iteration Allowed
int PLASMA_CYCLE;			// Number of plasma oscilations the simulation will run for.

/*****************************************************************************/
// Clear Memory
void ClearArrays();
// Calculation routines
void Ecalc();
void Bcalc();
// File Output
void statfile(char filepre[81]);
FILE *openfile(char filepre[81], char filesuf[3]);
FILE *openfile2(char filepre[81], char filesuf[3]);
// Exiting
double converg(double CMAX, double CMIN, double CPEAK, int i);
// Import Routines
int setup1(FILE *fp1);
int setup2(FILE *fp1);
// Exit routine
void ctrlc_handler(int);

/*****************************************************************************/
// Memory allocation routine
#include "memallocate.h"

// Defines sources	
#include "source.h"

// Plasma routines
// If included set plasma = 1 in main
#include "plasma.h"
		
// BC subroutines ('Retartd.h' - Retarded Time Absorbing BC, 'TubeBC.h' - Plasma Tube)
#include "Retard.h"
//#include "TubeBC.h"

// Output routines
#include "output.h"

/*****************************************************************************/
/////////
// MAIN /
/////////

int main(int argc, char*argv[])
{
  char filein[80], fileout[80];        	// File name
  FILE *file_str;                       // Input file
  FILE *file_vc, *file_fd;	        // Output files
  double timev;				// Time variable
  time_t tstart, tstop;                 // Program Starting and Stopping times
  int trem;                             // Used to calculate run time
  int i, ip, j, m;			// Iteration
  int size, allocate=0;			// allocated data size
  
  //Defaults
  FAIL_SAFE=10;        			// Fail Safe (Program will stop at iteration ###)
  PLASMA_CYCLE=10;			// Number of plasma cycles before program will stop.
  df = 1.0;                             
  Q_flag = 0;
  plasma = 1;
  fields = 0;
  frate = FAIL_SAFE;

  // Welcome
  time(&tstart);
  printf("\n\n");
  printf("     Welcome to FDTD w/ Plasma Fluid Equations\n");
  printf("=======================================================\n");
  printf("Version %3.1f                 Last Modified %i/%i/%i\n", pffdtdver, pffdtdmonth, pffdtdday, pffdtdyear);
  printf("Author: Jeffrey Ward\n");
  printf("        Utah State University\n");
  printf("        Logan, Utah\n");
  printf("=======================================================\n");
  printf("\n");

  // Get Input File
  if (argc > 1)
    {
      strcpy(filein, argv[1]);
      strcpy(fileout, argv[1]);
      if (argc > 2)
	{
	  strcpy(fileout, argv[2]);
	}
      if (argc > 3)
	{
	  plasma = 1;
	  FREQ_PLASMA = atof(argv[3]);
	}
      else
	df = 0;
      if (argc > 4)
	FREQ_COL = atof(argv[4]);
      if (argc > 5)
	FREQ_CYC = atof(argv[5]);
      if (argc > 6)
	ANGLE_E_CYC = atof(argv[6]);
      if (argc > 7)
	ANGLE_A_CYC = atof(argv[7]);
      if (argc >8)
	T = atof(argv[8]);
    }
  else      	
    {
      printf("Enter the name of the input file (no extentions): ");
      scanf(" %s",&filein);
      printf("Enter the name of the output file (no extentions): ");
      scanf(" %s",&fileout);
    }

  // Open DATA FILE - Error at this point returns a 1
  printf("OPENING DATA FILES \n"
  );
  file_str = openfile2(filein,".str");
  file_vc = openfile(fileout,".vc");		// Voltage / Current @ feed
  file_fd = openfile(fileout,".fd");		// Field Values

  // Set up Arrays
  printf("INSALIZING ARRAYS \n");
  // Read inital Sim. parameters (Grid Info)
  if (setup1(file_str) == 1)
    {
      printf("Error Reading %s.str file format\n",filein);
      exit(3);
    }
  // Allocate arrays
  size = sx*sy*sz*sizeof(double) + sx*sy*sizeof(double) + sx*sizeof(double) + sizeof(double);
  EX = darray4(1, sx, 1, sy, 1, sz, 0, 1);
  EY = darray4(1, sx, 1, sy, 1, sz, 0, 1);
  EZ = darray4(1, sx, 1, sy, 1, sz, 0, 1);
  allocate = allocate + 3*(size + 2*sx*sy*sz*sizeof(double));
  allocate = EMBCallocate(allocate);
  BX = darray4(1, sx, 1, sy, 1, sz, 0, 1);
  BY = darray4(1, sx, 1, sy, 1, sz, 0, 1);
  BZ = darray4(1, sx, 1, sy, 1, sz, 0, 1);
  allocate = allocate + 3*(size + 2*sx*sy*sz*sizeof(double));
  ERX = darray3(1, sx, 1, sy, 1, sz);
  ERY = darray3(1, sx, 1, sy, 1, sz);
  ERZ = darray3(1, sx, 1, sy, 1, sz);
  allocate = allocate + 3*size;
  Sloc = iarray2(1, Snum, 0, 5);
  allocate = allocate + Snum*6*sizeof(double) + 6*sizeof(double); 
  Spar = darray1(1, Snum);
  VOLT = darray1(1, Snum);
  CURRENT = darray1(1, Snum);
  allocate = allocate + 3*Snum*sizeof(double); 
  if (plasma == 1)
    allocate = PLASMAallocate(allocate);
    	
  //Clear Arrays
  ClearArrays();
  EMBCclear();			// Inisalize Arrays Used for Boundary Conditions
  if (plasma == 1)
    {
      PLASMAclear();		// Inisalize Arrays Used for Plasma
      Ninital();
    }

  // Read secondary Sim. parameters (Boundary Conditions)
  if (setup2(file_str) == 1)
    {
      printf("Error Reading %s.str file format\n",filein);
      Q_flag = 3;
    }

  // Verify plasma parameters (if any)
  if (plasma == 1)
    {
      printf("\t\\\\Plasma Parameters\n\tfp->%5.3f(MHz)\tfc->%5.3f(MHz)\tfg->%5.3f(MHz)\n\t@%5.3f elivation & %5.3f azmith\n",(FREQ_PLASMA/1e6),(FREQ_PLASMA*FREQ_COL/1e6),(FREQ_CYC/1e6),ANGLE_E_CYC,ANGLE_A_CYC);
      df = dt*FREQ_PLASMA; 
      printf("\t N_0 -> %5.3f, %5.3f, %5.3f 1/cc\n",N_0[0]*1e-6,N_0[1]*1e-6,N_0[2]*1e-6);
    }

  // Write header line for output files
  headvc(file_vc);
  headfd(file_fd);

  // Prepare for loops by taking over the Control-C interrupt
  if (signal(SIGINT, ctrlc_handler) == SIG_ERR)
    {
      printf(" Error with abot subroutine");
      exit(4);
    }
  printf("\nControl-C to exit early\n");

  // Finite Time part of FDTD
  printf("\n");
  printf("--------------------------------------------------------------------------------\n");
  timev = 0.0;
  i = 1;
  ip = 1000000000;

  // Note: C_flag < # is set so that false convergance are overlooked
  while ( Q_flag == 0 )
    {
      // Calculate Fields	(Finite Difference Part)
      // E
      if (plasma == 1)
	Ecalcmod();
      else
	Ecalc();
      EBCcalc();
      for (j=1;j<=Snum;j++)
	Esource(timev,j);
      // B
      Bcalc();
      // Plasma
      if (plasma == 1) //& ((ip*df*1e3) >= 1))
      {
	  Pcalc();
	  ip = 1;
      }
      // R
      for (j=1;j<=Snum;j++)
	Rcalc(j);

      // Output Results
      printf("\n%s It=%d(%5.3fP.C.):%fmV %fuA", fileout, i, (i*df), VOLT[1]*1e3, CURRENT[1]*1e6);
      //if (plasma == 1)
	//  for(m=0;m<NS;m++)
	  //    printf(" %f ",UX[sx/2][sy/2][sz/2][2][m]*1e3);
      if (((i-1)%frate==0) & (fields==1) )
      	{
      	  //printf(" Writing Data");
	  outputfd(file_fd, i, timev);
	}
      fprintf(file_vc,"%e", timev);
      for (j = 1; j <= Snum; j++)
	fprintf(file_vc,"\t%e\t%e", VOLT[j], CURRENT[j]);
      fprintf(file_vc,"\n");
 
      // Convergance

      // assuming all physics are documented in PLASMA_CYCLE
      if ((i*df) > PLASMA_CYCLE)
	Q_flag = 1;

      // Max Iteration Reached
      if ( i >= FAIL_SAFE )
	Q_flag = 1;

      // Check for Stability
       // Only checks main soucres
      //if ( ( CURRENT[1][i] > 1e3 ) | ( CURRENT[1][i] < -1e3 ) )
//	{
//	  printf("\n");
//	  printf("***************************\n");
//	  printf("* FDTD HAS BECOME UNSTABE *\n");
//	  printf("*   Exiting Calculation   *\n");
//	  printf("***************************\n");
//	  Q_flag = 1;
//        }

      // Update increments
      timev += dt;
      i += 1;
      ip += 1;

      // Use to exit for testing
      //       Q_flag = 1;

    }	
  printf("\n--------------------------------------------------------------------------------\n");
  printf("\n");

  // close DATA FILE
  printf("Closing Data Files \n");
  fclose(file_str);
  fclose(file_vc);
  fclose(file_fd);
  
  // clear memory
  printf("Clearing  Memory \n");
  freedarray4(EX, 1, sx, 1, sy, 1, sz, 0, 1);
  freedarray4(EY, 1, sx, 1, sy, 1, sz, 0, 1);
  freedarray4(EZ, 1, sx, 1, sy, 1, sz, 0, 1);
  EMBCfree();
  freedarray4(BX, 1, sx, 1, sy, 1, sz, 0, 1);
  freedarray4(BY, 1, sx, 1, sy, 1, sz, 0, 1);
  freedarray4(BZ, 1, sx, 1, sy, 1, sz, 0, 1);
  freedarray3(ERX, 1, sx, 1, sy, 1, sz);
  freedarray3(ERY, 1, sx, 1, sy, 1, sz);
  freedarray3(ERZ, 1, sx, 1, sy, 1, sz);
  if (plasma == 1)
    PLASMAfree();
  freeiarray2(Sloc, 1, Snum, 0, 5);
  freedarray1(Spar, 1, Snum);
  freedarray1(VOLT, 1, Snum);
  freedarray1(CURRENT, 1, Snum);
	
  // display program data
  time(&tstop);
  timev = difftime(tstop,tstart);
  printf("\nProgram Stats.\n");
  printf("\tUsed %d K bytes \n",(allocate/1024));
  trem = (int)timev / 3600;
  printf("\tElapsed Time %d:",trem);
  timev = timev - trem*3600;
  trem = (int)timev / 60;
  printf("%d:",trem);
  timev = timev - trem*60;
  printf("%5.2f\n\n",timev);

  if (Q_flag == 3)
    return 3;

  return 0;
}

/******************************************************************************/
///////////////////////
// Opens output files /
// 1 -> Write         /
// 2 -> Read          /
///////////////////////
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

/*****************************************************************************/
////////////////////////////////////
// Import Routines for Data        /
// 1 -> Prior to array allocation  /
// 2 -> BC, After array allocation /
////////////////////////////////////

int setup1(FILE *fp1)
{
  char tp1[80];
  char tp2[10],tp3[10],tp4[10];
  int i;
 
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
  if (sscanf(tp1,"%s\t%s\t%s",&tp2,&tp3,&tp4)!=3)
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
      //     if (Sloc[a][4] == 5)  // Error finder for gaussean derivitive sources
//	{
//	    if (Spar[a] > 1/8/dt)
//		return 1;
//	    if (Spar[a] < 2.5/FAIL_SAFE)
//		return 1;
//	    if (Spar[a] < 2.5*df/PLASMA_CYCLE)
//		return 1;
//	}
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

/*****************************************************************************/
/////////////////
// Clear Arrays /
/////////////////
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

/*****************************************************************************/
/////////////////////////////////////////////////
// Calculatest the Eletric Field at every point /
// Calculated at every possible point           /
/////////////////////////////////////////////////
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

/*****************************************************************************/
/////////////////////////////////////////////////////////////////////////////////
// Calculates the Magnetic Displacement at every point  /
//     Asssumes that E is Forced at boundary and ignores /
//     cells that don't effect E at boundary             /
////////////////////////////////////////////////////////////////////////////////
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

/*****************************************************************************/
/////////////////////////////////////
// Reassigns Control-C to exit loop /
/////////////////////////////////////
void ctrlc_handler(int sig)
{
  char c;
  
  signal(SIGINT, SIG_IGN);
  printf("\n INTERRUPTED. Quit?");
  c = getchar();
  if (c=='y'|c=='Y')
    Q_flag = 1;
  else
    signal(SIGINT, ctrlc_handler);
}

/*****************************************************************************/
///////////////////////////////////////////////
// Checks to see if simulations has converged /
///////////////////////////////////////////////
double converg(double CMAX, double CMIN, double CPEAK, int i)
{
  /*
  double ratio=100;
  
  if (i > 3);
  {
    if ((CURRENT[i-2] < CURRENT[i-1]) & (CURRENT[i-1] > CURRENT[i]))
      CMAX = CURRENT[i-1];
    if ((CURRENT[i-2] > CURRENT[i-1]) & (CURRENT[i-1] < CURRENT[i]))
      CMIN = CURRENT[i-1];
    if ((CMAX - CMIN) > CPEAK)
      CPEAK = CMAX - CMIN;
    ratio = (CMAX - CMIN) / CPEAK * 100;
  }
  return ratio;
  */
  return CMAX;
}
