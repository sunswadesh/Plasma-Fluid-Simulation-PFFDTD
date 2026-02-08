Wp = 123e6;
Nu = 0.123;
Wc = 345e6;

STR = ['./a.out ' 'dipole ' 'dipole ' num2str(Wp,3) ' ' num2str(Nu,3) ' ' num2str(Wc,3) ];
unix(STR);