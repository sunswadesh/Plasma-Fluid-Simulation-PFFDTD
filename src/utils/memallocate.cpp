#include "memallocate.h"
#include <malloc.h>
#include <stdlib.h>
#include <stdio.h>

#define NR_END 1
#define FREE_ARG char*

//////////////////////////////////////////////////////////////////////////////////////////
// Vector of doubles /
//////////////////////
double *darray1(int x1, int x2)
{
  double *A;

  // allocate array and set pointers to them
  A = (double *) malloc((size_t) ((x2-x1+1+NR_END)*sizeof(double)));
  if (!A)
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  return A-x1+NR_END;

}


//////////////////////////////////////////////////////////////////////////////////////////
// 2D Matrix of doubles /
/////////////////////////
double **darray2(int x1, int x2, int y1, int y2)
{
  long i, nrow=x2-x1+1, ncol=y2-y1+1;
  double **A;

  // allocate pointers to rows
  A = (double **) malloc((size_t) ((nrow+NR_END)*sizeof(double*)));
  if (!A)
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A += NR_END;
  A -= x1;
  
  // allocate rows and set pointers to them
  A[x1] = (double *) malloc((size_t) ((nrow*ncol+NR_END)*sizeof(double)));
  if (!A[x1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1] += NR_END;
  A[x1] -= y1;

  for(i=x1+1;i<=x2;i++)
    A[i] = A[i-1]+ncol;

  return A;
}

//////////////////////////////////////////////////////////////////////////////////////////
// 2D Matrix of ints /
//////////////////////
int **iarray2(int x1, int x2, int y1, int y2)
{
  long i, nrow=x2-x1+1, ncol=y2-y1+1;
  int **A;

  // allocate pointers to rows
  A = (int **) malloc((size_t) ((nrow+NR_END)*sizeof(int*)));
  if (!A)
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A += NR_END;
  A -= x1;
  
  // allocate rows and set pointers to them
  A[x1] = (int *) malloc((size_t) ((nrow*ncol+NR_END)*sizeof(int)));
  if (!A[x1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1] += NR_END;
  A[x1] -= y1;

  for(i=x1+1;i<=x2;i++)
    A[i] = A[i-1]+ncol;

  return A;
}

//////////////////////////////////////////////////////////////////////////////////////////
// 3D Matrix of doubles /
/////////////////////////
double ***darray3(int x1, int x2, int y1, int y2, int z1, int z2)
{
  long i, j, nrow=x2-x1+1, ncol=y2-y1+1, ndep=z2-z1+1;
  double ***A;

  // allocate pointers to pointers to arrays
  A = (double ***) malloc((size_t) ((nrow+NR_END)*sizeof(double**)));
  if (!A)
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A += NR_END;
  A -= x1;
  
  // allocate pointers to arrays and set pointers to them
  A[x1] = (double **) malloc((size_t) ((nrow*ncol+NR_END)*sizeof(double*)));
  if (!A[x1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1] += NR_END;
  A[x1] -= y1;

  // allocate array and set pointers to them
  A[x1][y1] = (double *) malloc((size_t) ((nrow*ncol*ndep+NR_END)*sizeof(double)));
  if (!A[x1][y1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1][y1] += NR_END;
  A[x1][y1] -= z1;
  
  // Assign locations
  for (j=y1+1;j<=y2;j++)
    A[x1][j] = A[x1][j-1]+ndep;
  for (i=x1+1;i<=x2;i++)
    {
      A[i] = A[i-1]+ncol;
      A[i][y1] = A[i-1][y1]+ncol*ndep;
      for(j=y1+1;j<=y2;j++)
	A[i][j] = A[i][j-1]+ndep;
    }
  return A;
}

//////////////////////////////////////////////////////////////////////////////////////////
// 4D Matrix of doubles /
/////////////////////////
double ****darray4(int x1, int x2, int y1, int y2, int z1, int z2, int m1, int m2)
// Allocates 4D pointer to pointer to array
{
  long i, j, k, nrow=x2-x1+1, ncol=y2-y1+1, ndep=z2-z1+1, noth=m2-m1+1;
  double ****A;
	
  // allocate pointers to pointers to pointers to arrays
  A = (double ****) malloc((size_t) ((nrow+NR_END)*sizeof(double***)));
  if (!A)
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A += NR_END;
  A -= x1;
		
  // allocate pointers to pointers to arrays and set pointers to them
  A[x1] = (double ***) malloc((size_t) ((nrow*ncol+NR_END)*sizeof(double**)));
  if (!A[x1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1] += NR_END;
  A[x1] -= y1;
	
  // allocate pointers to array and set pointers to them
  A[x1][y1] = (double **) malloc((size_t) ((nrow*ncol*ndep+NR_END)*sizeof(double*)));
  if (!A[x1][y1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1][y1] += NR_END;
  A[x1][y1] -= z1;
  
  // allocate array and set pointers to them
  A[x1][y1][z1] = (double *) malloc((size_t) ((nrow*ncol*ndep*noth+NR_END)*sizeof(double)));
  if (!A[x1][y1][z1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1][y1][z1] += NR_END;
  A[x1][y1][z1] -= m1;
  
  // Assign locations
  for(k=z1+1;k<=z2;k++)
    A[x1][y1][k] = A[x1][y1][k-1]+noth;
  for (j=y1+1;j<=y2;j++)
    {
      A[x1][j] = A[x1][j-1]+ndep;
      A[x1][j][z1] = A[x1][j-1][z1]+ndep*noth;
      for (k=z1+1;k<=z2;k++)
	A[x1][j][k] = A[x1][j][k-1]+noth;
    }
  for (i=x1+1;i<=x2;i++)
    {
      A[i] = A[i-1]+ncol;
      A[i][y1] = A[i-1][y1]+ncol*ndep;
      A[i][y1][z1] = A[i-1][y1][z1]+ncol*ndep*noth;
      for (k=z1+1;k<=z2;k++)
	A[i][y1][k] = A[i][y1][k-1]+noth;
      for (j=y1+1;j<=y2;j++)
	{
	  A[i][j] = A[i][j-1]+ndep;
	  A[i][j][z1] = A[i][j-1][z1]+ndep*noth;
	  for (k=z1+1;k<=z2;k++)
	    A[i][j][k] = A[i][j][k-1]+noth;
	}
    }
   return A;
}


//////////////////////////////////////////////////////////////////////////////////////////
// 5D Matrix of doubles /
/////////////////////////
double *****darray5(int x1, int x2, int y1, int y2, int z1, int z2, int m1, int m2, int n1, int n2)
// Allocates 5D pointer to pointer to array
{
  long i, j, k, l, nrow=x2-x1+1, ncol=y2-y1+1, ndep=z2-z1+1, noth=m2-m1+1, nothe=n2-n1+1;
  double *****A;
	
  // allocate pointers to pointers to pointers to arrays
  A = (double *****) malloc((size_t) ((nrow+NR_END)*sizeof(double****)));
  if (!A)
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A += NR_END;
  A -= x1;
		
  // allocate pointers to pointers to arrays and set pointers to them
  A[x1] = (double ****) malloc((size_t) ((nrow*ncol+NR_END)*sizeof(double***)));
  if (!A[x1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1] += NR_END;
  A[x1] -= y1;
	
  // allocate pointers to array and set pointers to them
  A[x1][y1] = (double ***) malloc((size_t) ((nrow*ncol*ndep+NR_END)*sizeof(double**)));
  if (!A[x1][y1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1][y1] += NR_END;
  A[x1][y1] -= z1;
  
  // allocate array and set pointers to them
  A[x1][y1][z1] = (double **) malloc((size_t) ((nrow*ncol*ndep*noth+NR_END)*sizeof(double*)));
  if (!A[x1][y1][z1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1][y1][z1] += NR_END;
  A[x1][y1][z1] -= m1;
  
 // allocate array and set pointers to them
  A[x1][y1][z1][m1] = (double *) malloc((size_t) ((nrow*ncol*ndep*noth*nothe+NR_END)*sizeof(double)));
  if (!A[x1][y1][z1][m1])
    {
      printf("Error in Allocating Memory");
      exit(2);
    }
  A[x1][y1][z1][m1] += NR_END;
  A[x1][y1][z1][m1] -= n1;

  // Assign locations
  for(l=m1+1;l<=m2;l++)
    A[x1][y1][z1][l] = A[x1][y1][z1][l-1]+nothe;
  for (k=z1+1;k<=z2;k++)
    {
      A[x1][y1][k] = A[x1][y1][k-1]+noth;
      A[x1][y1][k][m1] = A[x1][y1][k-1][m1]+noth*nothe;
      for (l=m1+1;l<=m2;l++)
	  A[x1][y1][k][l] = A[x1][y1][k][l-1]+nothe;
    }
  for (j=y1+1;j<=y2;j++)
    {
      A[x1][j] = A[x1][j-1]+ndep;
      A[x1][j][z1] = A[x1][j-1][z1]+ndep*noth;
      A[x1][j][z1][m1] = A[x1][j-1][z1][m1]+ndep*noth*nothe;
      for(l=m1+1;l<=m2;l++)
	  A[x1][j][z1][l] = A[x1][j][z1][l-1]+nothe;
      for (k=z1+1;k<=z2;k++)
      {
	  A[x1][j][k] = A[x1][j][k-1]+noth;
	  A[x1][j][k][m1] = A[x1][j][k-1][m1]+noth*nothe;
	  for (l=m1+1;l<=m2;l++)
	      A[x1][j][k][l] = A[x1][j][k][l-1]+nothe;
      }
     }
  for (i=x1+1;i<=x2;i++)
  {
      A[i] = A[i-1]+ncol;
      A[i][y1] = A[i-1][y1]+ncol*ndep;
      A[i][y1][z1] = A[i-1][y1][z1]+ncol*ndep*noth;
      A[i][y1][z1][m1] = A[i-1][y1][z1][m1]+ncol*ndep*noth*nothe;
      for(l=m1+1;l<=m2;l++)
	  A[i][y1][z1][l] = A[i][y1][z1][l-1]+nothe;
      for (k=z1+1;k<=z2;k++)
      {
	  A[i][y1][k] = A[i][y1][k-1]+noth;
	  A[i][y1][k][m1] = A[i][y1][k-1][m1]+noth*nothe;
	  for (l=m1+1;l<=m2;l++)
	      A[i][y1][k][l] = A[i][y1][k][l-1]+nothe;
      }
      for (j=y1+1;j<=y2;j++)
      {
	  A[i][j] = A[i][j-1]+ndep;
	  A[i][j][z1] = A[i][j-1][z1]+ndep*noth;
	  A[i][j][z1][m1] = A[i][j-1][z1][m1]+ndep*noth*nothe;
	  for(l=m1+1;l<=m2;l++)
	      A[i][j][z1][l] = A[i][j][z1][l-1]+nothe;
	  for (k=z1+1;k<=z2;k++)
	  {
	      A[i][j][k] = A[i][j][k-1]+noth;
	      A[i][j][k][m1] = A[i][j][k-1][m1]+noth*nothe;
	      for (l=m1+1;l<=m2;l++)
		  A[i][j][k][l] = A[i][j][k][l-1]+nothe;
	  }
      }
  }

   return A;
}


//////////////////////////////////////////////////////////////////////////////////////////
// Frees vector of doubles /
////////////////////////////
void freedarray1(double *A, int x1, int x2)
{
  free((FREE_ARG) (A+x1-NR_END));
}

//////////////////////////////////////////////////////////////////////////////////////////
// Frees 2D matrix of doubles /
///////////////////////////////
void freedarray2(double **A, int x1, int x2, int y1, int y2)
{
  free((FREE_ARG) (A[x1]+y1-NR_END));
  free((FREE_ARG) (A+x1-NR_END));
}

//////////////////////////////////////////////////////////////////////////////////////////
// Frees 2D matrix of ints /
////////////////////////////
void freeiarray2(int **A, int x1, int x2, int y1, int y2)
{
  free((FREE_ARG) (A[x1]+y1-NR_END));
  free((FREE_ARG) (A+x1-NR_END));
}

//////////////////////////////////////////////////////////////////////////////////////////
// Frees 3D matrix of doubles /
///////////////////////////////
void freedarray3(double ***A, int x1, int x2, int y1, int y2, int z1, int z2)
{
  free((FREE_ARG) (A[x1][y1]+z1-NR_END));
  free((FREE_ARG) (A[x1]+y1-NR_END));
  free((FREE_ARG) (A+x1-NR_END));
}

//////////////////////////////////////////////////////////////////////////////////////////
// Frees 4D matrix of doubles /
///////////////////////////////
void freedarray4(double ****A, int x1, int x2, int y1, int y2, int z1, int z2, int m1, int m2)
{
  free((FREE_ARG) (A[x1][y1][z1]+m1-NR_END));
  free((FREE_ARG) (A[x1][y1]+z1-NR_END));
  free((FREE_ARG) (A[x1]+y1-NR_END));
  free((FREE_ARG) (A+x1-NR_END));
}

//////////////////////////////////////////////////////////////////////////////////////////
// Frees 5D matrix of doubles /
///////////////////////////////
void freedarray5(double *****A, int x1, int x2, int y1, int y2, int z1, int z2, int m1, int m2, int n1, int n2)
{
  free((FREE_ARG) (A[x1][y1][z1][m1]+n1-NR_END));
  free((FREE_ARG) (A[x1][y1][z1]+m1-NR_END));
  free((FREE_ARG) (A[x1][y1]+z1-NR_END));
  free((FREE_ARG) (A[x1]+y1-NR_END));
  free((FREE_ARG) (A+x1-NR_END));
}
