clear

string(1,:) = 'dipole2xG1000.vc';
string(2,:) = 'dipole2xG1090.vc';
%string(3,:) = 'run3.vc';
%string(4,:) = 'run4.vc';
%string(5,:) = 'run5.vc';
%tring(6,:) = 'run6.vc';

sn = 1;

for i = 1:size(string,1)

% Load data
temp=load(string(i,:));
[m n]=size(temp);
index=temp(1,:);
values=temp(2:m,:);

clear temp;

% Retrieve data
T = values(:,1);
dt = T(2) - T(1);
V = values(:,2*sn);
C = values(:,2*sn+1);

w = pi*2*dt*0.5e6:0.00001:pi*2*dt*10e6;

V_dtft = dtft(V',w);
I_dtft = dtft(C',w);
Z_dtft(i,:) = V_dtft./I_dtft;


Cap = 1e-12;
XC_dtft = -i./w/Cap;


%   figure(3)
%   subplot(2,1,1)
%   plot(T,V)
%   ylabel('Voltage')
%   subplot(2,1,2)
%   plot(T,C)
%   ylabel('Current')
%  
%  figure(10)
%  subplot(2,1,1)
%  plot(w/dt/1e6/pi/2,log10(abs(V_dtft)))
%  axis tight
%  ylabel('FFT_V')
%  subplot(2,1,2)
%  plot(w/dt/1e6/pi/2,log10(abs(I_dtft)))
%  axis tight
%  ylabel('FFT_I')
%  
%  figure(11)
%  plot(w/dt/1e6/pi/2, 20*log10(abs(Z_dtft)), w/dt/1e6/pi/2,20*log10(abs(XC_dtft))-220)
%  axis tight
%  ylabel('FFT_Z')
%  
%  figure(12)
%  plot(w/dt/1e6/pi/2, 20*log10(abs(Z_dtft))-(20*log10(abs(XC_dtft))-220))
%  axis tight
%  ylabel('FFT_Z')
%  
%  figure(13)
%  plot(w/dt/1e6/pi/2, 20*log10(abs(Z_dtft./XC_dtft)))
%  axis tight
%  ylabel('FFT_Z')

end


XC_dtft = ones(size(string,1),1)*XC_dtft;
figure(1)
subplot(2,1,1)
plot(w/dt/1e6/pi/2, 20*log10(abs(Z_dtft./XC_dtft)))
subplot(2,1,2)
plot(w/dt/1e6/pi/2, 180*angle(Z_dtft)/pi)

figure(2)
subplot(2,1,1)
plot(w/dt/1e6/pi/2, 20*log10(real(Z_dtft)))
subplot(2,1,2)
plot(w/dt/1e6/pi/2, 20*log10(imag(Z_dtft)))





