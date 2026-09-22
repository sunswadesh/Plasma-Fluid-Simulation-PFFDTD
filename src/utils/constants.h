#ifndef CONSTANTS_H
#define CONSTANTS_H

// Mathematical Constants
#define PI 3.14159265359

// Physical Constants (SI Units)
#define MU_0 1.25663706143591729538505735331180115367886775e-6
#define EPSILON_0 8.85418781762038985053656303171075026060837e-12
#define C 2.998e8
 
 // Indexing Macros for Flattened 1D Arrays
 // Assumes 0-based indexing for internal calculation, but i,j,k can be 1-based from loops
 // 3D Arrays: (i, j, k)
 // Size: (sx+1)*(sy+1)*(sz+1)
 #define IDX3(i,j,k) ( ((i)*(sy+1) + (j))*(sz+1) + (k) )
 
 // 4D Arrays: (i, j, k, l)
 // Size: (sx+1)*(sy+1)*(sz+1)*2
 #define IDX4(i,j,k,l) ( (((i)*(sy+1) + (j))*(sz+1) + (k))*2 + (l) )

// Time-level rotation indices.
//
// The field/plasma updates used to copy whole grids every step just to keep
// time history ("save old values"). Instead, these indices rotate which level
// slot means "old"/"current", so no copies are needed:
//   - 2-level E/B fields: *_old holds the previous step, *_cur the newest.
//   - 3-level U/N fields: *_0 oldest, *_1 middle, *_2 newest.
// Each kernel swaps/rotates its own indices once per step, after its update.
extern int tlE_old, tlE_cur, tlB_old, tlB_cur;
extern int tlU_0, tlU_1, tlU_2, tlN_0, tlN_1, tlN_2;

#endif // CONSTANTS_H
