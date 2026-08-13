function Q_Array = P2G00(Q_Array, Q_value_Particle, x_i, y_j, z_k, w_i, w_j, w_k, N_grid_x, N_grid_y, N_grid_z)

if ((x_i >=1 && x_i<=N_grid_x-1) && (y_j >= 1 && y_j<=N_grid_y-1)  && (z_k >= 1 && z_k<=N_grid_z-1))
          Q_Array(x_i,y_j,z_k) = Q_Array(x_i,y_j,z_k) + Q_value_Particle*(1-w_i)*(1-w_j)*(1-w_k);
          Q_Array(x_i+1,y_j,z_k) = Q_Array(x_i+1,y_j,z_k) + Q_value_Particle*(w_i)*(1-w_j)*(1-w_k);
          Q_Array(x_i,y_j+1,z_k) = Q_Array(x_i,y_j+1,z_k) + Q_value_Particle*(1-w_i)*(w_j)*(1-w_k);
          Q_Array(x_i,y_j,z_k+1) = Q_Array(x_i,y_j,z_k+1) + Q_value_Particle*(1-w_i)*(1-w_j)*(w_k);
          Q_Array(x_i+1,y_j+1,z_k) = Q_Array(x_i+1,y_j+1,z_k) + Q_value_Particle*(w_i)*(w_j)*(1-w_k);
          Q_Array(x_i+1,y_j,z_k+1) = Q_Array(x_i+1,y_j,z_k+1) + Q_value_Particle*(w_i)*(1-w_j)*(w_k);
          Q_Array(x_i,y_j+1,z_k+1) = Q_Array(x_i,y_j+1,z_k+1) + Q_value_Particle*(1-w_i)*(w_j)*(w_k);
          Q_Array(x_i+1,y_j+1,z_k+1) = Q_Array(x_i+1,y_j+1,z_k+1) + Q_value_Particle*(w_i)*(w_j)*(w_k); 
       
end

