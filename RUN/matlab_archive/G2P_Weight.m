function A_out = G2P_Weight(Array_In, x_i, y_j, z_k, p_i, p_j, p_k)
       
         A_1 = Array_In(x_i,y_j,z_k)*(1-p_i) *(1-p_j)*(1-p_k);  % 0 0 0
         A_2 = Array_In(x_i,y_j+1,z_k)*(1-p_i)*(p_j)*(1-p_k); %0 1 0
         A_3 = Array_In(x_i+1,y_j,z_k)*(p_i)*(1-p_j)*(1-p_k); %1 0 0
         A_4 = Array_In(x_i,y_j,z_k+1)*(1-p_i)*(1-p_j)*(p_k); %0 0 1
         A_5 = Array_In(x_i+1,y_j+1,z_k)*(p_i)*(p_j)*(1-p_k); % 1 1 0
         A_6 = Array_In(x_i+1,y_j,z_k+1)*(p_i)*(1-p_j)*(p_k); % 1 0 1
         A_7 = Array_In(x_i,y_j+1,z_k+1)*(1-p_i)*(p_j)*(p_k); % 0 1 1
         A_8 = Array_In(x_i+1,y_j+1,z_k+1)*(p_i)*(p_j)*(p_k); % 1 1 1 
         
         A_out = [A_1 A_2 A_3 A_4 A_5 A_6 A_7 A_8];
                 
