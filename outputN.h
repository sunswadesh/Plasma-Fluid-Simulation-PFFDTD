// Outputs to files
// For Version 1.8+

// Author: Jeff Ward
// Last Modified 1/28/05

/*****************************************************************************/
/////////////////////////////
// Header for Source output /
/////////////////////////////
void headvc(FILE *file_vc)
{
  int i;

  fprintf(file_vc,"0");
  for (i=1; i<=Snum; i++)
    fprintf(file_vc,"\t%d1\t%d2",i,i);
  fprintf(file_vc,"\n");

}

/*****************************************************************************/
////////////////////////////
// Header of Fields output /
////////////////////////////
void headfd(FILE *file_fd)
{
  int i,j,k;

  // Field Id
  fprintf(file_fd,"0");
  for (i = floc[0][0]; i <= floc[1][0]; i++)
    for (j = floc[0][1]; j <= floc[1][1]; j++)
      for (k = floc[0][2]; k <= floc[1][2]; k++)
	{
	  if (fout[0] == 1)
	    fprintf(file_fd,"\t11\t12\t13");
	  if (fout[1] == 1)
	    fprintf(file_fd,"\t21\t22\t23");
	  if (plasma == 1)
	    {
	      if (fout[2] == 1)
		fprintf(file_fd,"\t31\t32\t33");
	      if (fout[3]== 1)
		fprintf(file_fd,"\t40");
	      if (fout[4] == 1)
		fprintf(file_fd,"\t51\t52\t53");
	      if (fout[5]== 1)
		fprintf(file_fd,"\t60");
	    }
	}
  fprintf(file_fd,"\n");
  // Location Id i
  fprintf(file_fd,"0");
  for (i = floc[0][0]; i <= floc[1][0]; i++)
    for (j = floc[0][1]; j <= floc[1][1]; j++)
      for (k = floc[0][2]; k <= floc[1][2]; k++)
	{
	  if (fout[0] == 1)
	    fprintf(file_fd,"\t%d\t%d\t%d",i,i,i);
	  if (fout[1] == 1)
	    fprintf(file_fd,"\t%d\t%d\t%d",i,i,i);
	  if (plasma == 1)
	    {
	      if (fout[2] == 1)
		fprintf(file_fd,"\t%d\t%d\t%d",i,i,i);
	      if (fout[3]== 1)
		fprintf(file_fd,"\t%d",i);
	      if (fout[4] == 1)
		fprintf(file_fd,"\t%d\t%d\t%d",i,i,i);
	      if (fout[5]== 1)
		fprintf(file_fd,"\t%d",i);

	    }
	}
  fprintf(file_fd,"\n");
  // Location Id j
  fprintf(file_fd,"0");
  for (i = floc[0][0]; i <= floc[1][0]; i++)
    for (j = floc[0][1]; j <= floc[1][1]; j++)
      for (k = floc[0][2]; k <= floc[1][2]; k++)
	{
	  if (fout[0] == 1)
	    fprintf(file_fd,"\t%d\t%d\t%d",j,j,j);
	  if (fout[1] == 1)
	    fprintf(file_fd,"\t%d\t%d\t%d",j,j,j);
	  if (plasma == 1)
	    {
	      if (fout[2] == 1)
		fprintf(file_fd,"\t%d\t%d\t%d",j,j,j);
	      if (fout[3]== 1)
		fprintf(file_fd,"\t%d",j);
	      if (fout[4] == 1)
	      	fprintf(file_fd,"\t%d\t%d\t%d",j,j,j);
	      if (fout[5]== 1)
	      	fprintf(file_fd,"\t%d",j);
	    }
	}
  fprintf(file_fd,"\n");
  // Location Id k
  fprintf(file_fd,"0");
  for (i = floc[0][0]; i <= floc[1][0]; i++)
    for (j = floc[0][1]; j <= floc[1][1]; j++)
      for (k = floc[0][2]; k <= floc[1][2]; k++)
	{
	  if (fout[0] == 1)
	    fprintf(file_fd,"\t%d\t%d\t%d",k,k,k);
	  if (fout[1] == 1)
	    fprintf(file_fd,"\t%d\t%d\t%d",k,k,k);
	  if (plasma == 1)
	    {
	      if (fout[2] == 1)
		fprintf(file_fd,"\t%d\t%d\t%d",k,k,k);
	      if (fout[3]== 1)
		fprintf(file_fd,"\t%d",k);
	      if (fout[4] == 1)
		fprintf(file_fd,"\t%d\t%d\t%d",k,k,k);
	      if (fout[5]== 1)
	      	fprintf(file_fd,"\t%d",k);
	    }
	}
  fprintf(file_fd,"\n");
}

/*****************************************************************************/
/////////////////////
// Output of Fields /
/////////////////////
void outputfd(FILE *file_fd, int a, double timev)
{
  int i, j, k;

  // Output Time
  fprintf(file_fd,"%e",timev);
  
  // Output Fields
  for (i = floc[0][0]; i <= floc[1][0]; i++)
    for (j = floc[0][1]; j <= floc[1][1]; j++)
      for (k = floc[0][2]; k <= floc[1][2]; k++)
	{ 
	  if (fout[0] == 1)
	    fprintf(file_fd,"\t%e\t%e\t%e",EX[i][j][k][1], EY[i][j][k][1], EZ[i][j][k][1]);
	  if (fout[1] == 1)
	    fprintf(file_fd,"\t%e\t%e\t%e",BX[i][j][k][1], BY[i][j][k][1], BZ[i][j][k][1]);
	  if (plasma == 1)
	    {
	      if (fout[2] == 1)
		fprintf(file_fd,"\t%e\t%e\t%e",UX[i][j][k][1][0], UY[i][j][k][1][0], UZ[i][j][k][1][0]);
	      if (fout[3]== 1)
		//fprintf(file_fd,"\t%e",(N[i][j][k][1][0]-N_0[0]));// Uncomment this line and comment the one below to restore jeff's code.
                fprintf(file_fd,"\t%e",N_0[i][j][k][1][0]);//Write only ambient density values
		//printf("N0=%f,i=%d,j=%d,k=%d\n",N_0[i][j][k][0][0],i,j,k);
	      if (fout[4] == 1)
	      	fprintf(file_fd,"\t%e\t%e\t%e",UX[i][j][k][1][1], UY[i][j][k][1][1], UZ[i][j][k][1][1]);
	      //if (fout[5]== 1)
	      	//fprintf(file_fd,"\t%e",(N[i][j][k][1][1]-N_0[i][j][k][1][0]));
 		//fprintf(file_fd,"\t%e",(N[i][j][k][1][1]-N_0[1]));

	    }
	}
		
  fprintf(file_fd,"\n");
 }

