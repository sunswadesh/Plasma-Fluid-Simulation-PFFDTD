% Function to calculate DTFT, input vector X(n), frequency abscissa vector W, returns vector Y
function Y = dtft(X,W)

k = 0:size(X,2)-1;
E_wk = exp(-i*k'*W); % Create grid by multiplying N by 1 with 1 by M
Y = X*E_wk;
