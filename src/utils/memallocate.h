#ifndef MEMALLOCATE_H
#define MEMALLOCATE_H

// Function Prototypes
double *darray1(int x1, int x2);
double **darray2(int x1, int x2, int y1, int y2);
int **iarray2(int x1, int x2, int y1, int y2);
double ***darray3(int x1, int x2, int y1, int y2, int z1, int z2);
double ****darray4(int x1, int x2, int y1, int y2, int z1, int z2, int m1, int m2);
double *****darray5(int x1, int x2, int y1, int y2, int z1, int z2, int m1, int m2, int n1, int n2);

void freedarray1(double *A, int x1, int x2);
void freedarray2(double **A, int x1, int x2, int y1, int y2);
void freeiarray2(int **A, int x1, int x2, int y1, int y2);
void freedarray3(double ***A, int x1, int x2, int y1, int y2, int z1, int z2);
void freedarray4(double ****A, int x1, int x2, int y1, int y2, int z1, int z2, int m1, int m2);
void freedarray5(double *****A, int x1, int x2, int y1, int y2, int z1, int z2, int m1, int m2, int n1, int n2);

#endif // MEMALLOCATE_H
