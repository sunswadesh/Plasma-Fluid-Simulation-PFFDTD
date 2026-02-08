% Sourceout - Plots Source Voltage, Current and Impedance
%             for the Plasma FDTD code output
%             version 1.4
%	Function [ZF, Freq] = Sourceout ('text',padd,sn,pt)
%       input
%           name of the file to be viewed
%           padd - # of points used to data file,
%                  If file is smaller data will be padded
%                  ( increase Freq resolution )
%           sn - Source number (If more then one source is used)
%           pt - plot parameters (NO COLOR) i.e. '*:'
%       output
%           ZF - Impedance in Frequincy Domain
%           Freq - Frequincy Scale for Impedance
%           graph of values
% by Jeff Ward
% last modified 11/25/02

%function [ZF, Freq] = Sourceout(string,padd,sn,pt)
%clear;
string = 'dipole.vc';
padd = 0;
sn = 1;
%inisalize
vector_padd=ones(1,padd);

% Load data
temp=load(string);
[m n]=size(temp);
index=temp(1,:);
values=temp(2:m,:);

% Retrieve data
T = values(:,1);
dt = T(2) - T(1);
V = values(:,2*sn);
C = values(:,2*sn+1);

%Adjust for low freq resolution
if (m-1)<padd
    TP = T';
    for i=1:padd-m+1
        TP(m-1+i)=T(m-1)+i*dt;
    end 
    VP = [V' vector_padd(1:padd-m+1).*V(length(V))];
    CP = [C' vector_padd(1:padd-m+1).*C(length(C))];
else
    TP = T(1:padd);
    VP = V(1:padd);
    CP = C(1:padd);
end

pad = 0;

T_min = T(size(T,1),1);
pts_T = 1:pad;
T_pts = T_min*ones(pad,1) + dt*pts_T';

%T = [T;T_pts]
%V =[V;zeros(pad,1)];
%C =[C;zeros(pad,1)];

%find FFT
VF = fftshift(fft(V));
CF = fftshift(fft(C));

%find Z(f)
ZF = VF./CF;
%ZT = VP./CP;
%ZF = fft(ZT);

L = size(ZF,1)

freq_factor = 1/dt/size(T,1);
freq_pts = [-size(T,1)/2:size(T,1)/2-1]*freq_factor/1e6;

%freq_pts = [-1/2:1/L:1/2-1/L]*freq_factor;

figure(2)
subplot(2,1,1)
plot(T,V)
ylabel('Voltage')
subplot(2,1,2)
plot(T,C)
ylabel('Current')

figure(3)
subplot(3,1,1)
plot(freq_pts,log10(abs(VF)))
axis tight
ylabel('FFT_V')
subplot(3,1,2)
plot(freq_pts,log10(abs(CF)))
axis tight
ylabel('FFT_C')
subplot(3,1,3)
plot(freq_pts,log10(abs(ZF)),'*')
axis tight
ylabel('FFT_Z')

break

%find Freq scale
Freq=[0:1/(dt*(length(TP))):(length(TP)-1)/(dt*(length(TP)))];

%graph V(t)
figure(3);
subplot(2,1,1);
hold on;
plot(TP.*1e9,VP,'b-');
plot(TP.*1e9,zeros(1,padd),'k--');
xlabel('Time (nsec)'); 
ylabel('Source Voltage');
hold off;


%graph C(t)
subplot(2,1,2);
hold on;
plot(TP.*1e9,CP,'b-');
plot(TP.*1e9,zeros(1,padd),'k');
xlabel('Time (nsec)');
ylabel('Source Current');
hold off;

%graph real Z(f)
figure(1);
subplot(2,1,1);
hold on;
plot(Freq./1e6,abs(real(ZF)),strcat('b',pt));
xlabel('Frequency (M Hz)');
ylabel('Real Z');
hold off;

%graph imag Z(f)
subplot(2,1,2);
hold on;
plot(Freq./1e6,imag(ZF),strcat('r',pt));
xlabel('Frequency (M Hz)');
ylabel('Imag Z');
hold off;

%graph |Z(f)|
figure(2);
subplot(2,1,1);
hold on;
plot(Freq./1e6,abs(ZF),strcat('b',pt));
xlabel('Frequency (M Hz)');
ylabel('|Z|');
hold off;

%graph angle Z(f)
subplot(2,1,2);
hold on;
plot(Freq./1e6,angle(ZF),strcat('r',pt));
xlabel('Frequency (M Hz)');
ylabel('Phase Z');
hold off;
