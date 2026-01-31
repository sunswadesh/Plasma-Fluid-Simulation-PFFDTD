#ifndef PLASMA_H
#define PLASMA_H

//Defaults
#define ME 9.1066e-31                           // Mass of electron
#define QE -1.6021917e-19                       // Charge of electron
#define AMU 1.6605e-27                          // AMU -> kg
#define K 1.380622e-23                          // Boltzmans Constant

#define NS 3                                    // Number of species (NS=1 is only electrons)

// Global Variables (Extern)
extern double FREQ_PLASMA;
extern double FREQ_COL;
extern double FREQ_CYC;
extern double ANGLE_E_CYC;
extern double ANGLE_A_CYC;
extern double UX_0;
extern double UY_0;
extern double UZ_0;
extern double T;
extern double Charge;

extern double N_0[NS];                                 // initial density of species 
extern double M[NS];                                   // Array of masses for species
extern double Q[NS];                                   // Array of charges for species

extern double *****UX, *****UY, *****UZ;	        // Partical Movement NOTE: [x][y][z][time][species:0=electron,1+=ions] 1/26/05
extern double *****N;					// Density (same as UX)
extern double ***SIG;					// Conductivity (used to define plasma field)
extern double ***QF;                                   // Charging Factor (for electrons only

// Externs for Field Arrays used in plasma.cpp
extern double ****EX, ****EY, ****EZ;
extern double ****BX, ****BY, ****BZ;
extern double ***ERX, ***ERY, ***ERZ;
extern double dt, dx, dy, dz;
extern int sx, sy, sz;

// Function Prototypes
int PLASMAallocate(int allocate);
void PLASMAclear();
void PLASMAfree();

void Ninital();
void Ucalc();
void Ncalc();
void Ecalcmod();
void Pcalc();
void UBCcalc();
void NBCcalc();

#endif // PLASMA_H
