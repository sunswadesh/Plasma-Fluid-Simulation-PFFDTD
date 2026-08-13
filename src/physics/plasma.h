#ifndef PLASMA_H
#define PLASMA_H

//Defaults
#define ME 9.1066e-31                           // Mass of electron
#define QE -1.6021917e-19                       // Charge of electron
#define AMU 1.6605e-27                          // AMU -> kg
#define K 1.380622e-23                          // Boltzmans Constant
#define N_MIN_RATIO 1.0e-6                      // Density Floor Ratio (relative to N0)
#define V_MAX_RATIO 0.1                         // Velocity Clamp Ratio (relative to C)

#define NS 3                                    // Number of species (NS=1 is only electrons)

 // 5D Arrays: (i, j, k, l, m)
 // Size: (sx+1)*(sy+1)*(sz+1)*3*NS
 // Last dim m runs 0..NS-1. Next dim l runs 0..2 (time).
 #define IDX5(i,j,k,l,m) ( ((((i)*(sy+1) + (j))*(sz+1) + (k))*3 + (l))*NS + (m) )

 // Spatial density index: (i, j, k, m) — no time dimension
 // Size: (sx+1)*(sy+1)*(sz+1)*NS
 #define IDX_N0(i,j,k,m) ( (((i)*(sy+1) + (j))*(sz+1) + (k))*NS + (m) )

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

extern double *UX, *UY, *UZ;	        // Partical Movement (Flat 1D: IDX5)
extern double *N;					// Density (Flat 1D: IDX5)
extern double *N0_SPATIAL;			// Spatially-varying ambient density (Flat 1D: IDX3*NS)
extern double *SIG;					// Conductivity (Flat 1D: IDX3)
extern double *QF;                                   // Charging Factor (Flat 1D: IDX3)

// Sheath parameters
extern int Sd;                                  // Sheath width in cells (0 = no sheath)

// Externs for Field Arrays used in plasma.cpp
extern double *EX, *EY, *EZ;
extern double *BX, *BY, *BZ;
extern double *ERX, *ERY, *ERZ;
extern double dt, dx, dy, dz;
extern int sx, sy, sz;

// Function Prototypes
int PLASMAallocate(int allocate);
void PLASMAclear();
void PLASMAfree();
void ApplySheath();
void DumpN0Line(const char *fileout);
#ifdef SHEATH_LEGACY_SIG_SEED
void ApplySheathLegacySigSeed();
#endif

void Ninital();
void Ucalc();
void Ncalc();
void Ecalcmod();
void Pcalc();
void UBCcalc();
void NBCcalc();

#endif // PLASMA_H
