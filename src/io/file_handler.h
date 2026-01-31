#ifndef FILE_HANDLER_H
#define FILE_HANDLER_H

#include <stdio.h>

// File Opening
FILE *openfile(char filepre[81], char filesuf[3]);
FILE *openfile2(char filepre[81], char filesuf[3]);

// Setup / Import
int setup1(FILE *fp1);
int setup2(FILE *fp1);

// Utility
void ClearArrays();

#endif // FILE_HANDLER_H
