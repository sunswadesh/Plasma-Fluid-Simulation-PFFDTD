% Function to calculate DTFT, input vector X(n), frequency abscissa vector W, returns vector Y
function Y = dtftfor(X,W)

k = 0:size(X,2)-1;

Y=zeros(1,length(W));

for j=1:length(W)
       E_wk = exp(-i*k*W(j)); 
       Y(j)=X*E_wk';   
end


