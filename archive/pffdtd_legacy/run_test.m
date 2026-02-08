%unix('g++ ~/PFFDTD/pffdtd.cpp');
%unix('cp ~/PFFDTD/a.out ~/es_test_runs/');
%cd ~/es_test_runs/;
%unix('./a.out dipole dipole90 0.438e6 0.1 1.16e6 90 0')
%unix('./a.out dipole_2x dipole2x00 0.438e6 0.1 1.16e6 0 0')
%unix('./a.out dipole_2x90 dipole2x90 0.438e6 0.1 1.16e6 90 0')
unix('./a.out patch patch01')
%unix('./a.out dipole_2x90 dipole2xG1090 0.438e7 0.1 1.16e7 90 0')