clear

string = 'patch01.vc';
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

w = pi*2*dt*1e6:0.00001:pi*2*dt*10e6;

V_dtft = dtft(V',w);
I_dtft = dtft(C',w);
Z_dtft = V_dtft./I_dtft;


Cap = 1e-12;
XC_dtft = -i./w/Cap;


 figure(3)
 subplot(2,1,1)
 plot(T,V)
 ylabel('Voltage')
 subplot(2,1,2)
 plot(T,C)
 ylabel('Current')

figure(10)
subplot(2,1,1)
plot(w/dt/1e6/pi/2,log10(abs(V_dtft)))
axis tight
ylabel('FFT_V')
subplot(2,1,2)
plot(w/dt/1e6/pi/2,log10(abs(I_dtft)))
axis tight
ylabel('FFT_I')

%normalization point
norm_diff = 20*log10(abs(XC_dtft(size(XC_dtft,2)))) - 20*log10(abs(Z_dtft(size(Z_dtft,2)))); 


figure(11)
plot(w/dt/1e6/pi/2, 20*log10(abs(Z_dtft)), w/dt/1e6/pi/2,20*log10(abs(XC_dtft))-norm_diff)
axis tight
ylabel('FFT_Z')

figure(12)
plot(w/dt/1e6/pi/2, 20*log10(abs(Z_dtft))-(20*log10(abs(XC_dtft))))
axis tight
ylabel('FFT_Z')


