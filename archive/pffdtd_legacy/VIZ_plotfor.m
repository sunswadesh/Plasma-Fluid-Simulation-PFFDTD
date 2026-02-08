clear all

string = 'dipole05107590.vc';
sn = 1;

% Load data
temp=load(string);
[m n]=size(temp);
index=temp(1,:);
values=temp(2:m,:);

clear temp;

% Retrieve data
T = values(:,1);
dt = T(2) - T(1);
V = values(:,2*sn);
C = values(:,2*sn+1);

w = pi*2*dt*3.5e6:0.0000001:pi*2*dt*15e6;

V_dtft = dtftfor(V',w);
I_dtft = dtftfor(C',w);
Z_dtft = V_dtft./I_dtft;


Cap = 1e-10;
XC_dtft = -i./w/Cap;


 figure(31)
 subplot(2,1,1)
 plot(T,V)
 title('plasma frequency 5MHz')
 ylabel('Voltage')
 subplot(2,1,2)
 plot(T,C)
 title('plasma frequency 5MHz')
 ylabel('Current')

figure(101)
subplot(2,1,1)
plot(w/dt/1e6/pi/2,log10(abs(V_dtft)))
axis tight
title('plasma frequency 5MHz')
ylabel('FFT_V')
subplot(2,1,2)
plot(w/dt/1e6/pi/2,log10(abs(I_dtft)))
axis tight
title('plasma frequency 5MHz')
ylabel('FFT_I')

%normalization point
norm_diff = 20*log10(abs(XC_dtft(size(XC_dtft,2)))) - 20*log10(abs(Z_dtft(size(Z_dtft,2)))); 


figure(111)
plot(w/dt/1e6/pi/2, 20*log10(abs(Z_dtft)), w/dt/1e6/pi/2,20*log10(abs(XC_dtft))-norm_diff)
axis tight
title('plasma frequency 5MHz')
ylabel('FFT_Z')

figure(121)
plot(w/dt/1e6/pi/2, 20*log10(abs(Z_dtft))-(20*log10(abs(XC_dtft))),'*')
axis tight
title('plasma frequency  5MHz')
ylabel('FFT_Z')


