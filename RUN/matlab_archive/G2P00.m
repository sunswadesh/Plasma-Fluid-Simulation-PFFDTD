function [E_Field_At_Particle, B_Field_At_Particle] = G2P00(E_Array_x_n, E_Array_y_n, E_Array_z_n, B_Array_x_n, B_Array_y_n, B_Array_z_n, Particle_Vector_tt, N_grid_x, N_grid_y, N_grid_z)

E_Field_At_Particle = zeros(3,1);
B_Field_At_Particle = zeros(3,1);

Particle_Vector_tt;

        x_i = Particle_Vector_tt(1,1);
        y_j = Particle_Vector_tt(2,1);
        z_k = Particle_Vector_tt(3,1);
        
        p_i = Particle_Vector_tt(4,1);
        p_j = Particle_Vector_tt(5,1);
        p_k = Particle_Vector_tt(6,1);
        
        
        %%%% interpolate grid to particle scheme.
   if ((x_i >=1 && x_i<=N_grid_x-1) && (y_j >= 1 && y_j<=N_grid_y-1)  && (z_k >= 1 && z_k<=N_grid_z-1))       
       
       Ex_1 =  E_Array_x_n(x_i,y_j,z_k)*(1-p_i) *(1-p_j)*(1-p_k);  % 0 0 0
         Ex_2 = E_Array_x_n(x_i,y_j+1,z_k)*(1-p_i)*(p_j)*(1-p_k); %0 1 0
         Ex_3 = E_Array_x_n(x_i+1,y_j,z_k)*(p_i)*(1-p_j)*(1-p_k); %1 0 0
         Ex_4 = E_Array_x_n(x_i,y_j,z_k+1)*(1-p_i)*(1-p_j)*(p_k); %0 0 1
         Ex_5 =  E_Array_x_n(x_i+1,y_j+1,z_k)*(p_i)*(p_j)*(1-p_k); % 1 1 0
         Ex_6 =  E_Array_x_n(x_i+1,y_j,z_k+1)*(p_i)*(1-p_j)*(p_k); % 1 0 1
         Ex_7 =   E_Array_x_n(x_i,y_j+1,z_k+1)*(1-p_i)*(p_j)*(p_k); % 0 1 1
         Ex_8 =  E_Array_x_n(x_i+1,y_j+1,z_k+1)*(p_i)*(p_j)*(p_k); % 1 1 1 
%         
        Ey_1 =  E_Array_y_n(x_i,y_j,z_k)*(1-p_i) *(1-p_j)*(1-p_k);  % 0 0 0
         Ey_2 = E_Array_y_n(x_i,y_j+1,z_k)*(1-p_i)*(p_j)*(1-p_k); %0 1 0
         Ey_3 = E_Array_y_n(x_i+1,y_j,z_k)*(p_i)*(1-p_j)*(1-p_k); %1 0 0
         Ey_4 = E_Array_y_n(x_i,y_j,z_k+1)*(1-p_i)*(1-p_j)*(p_k); %0 0 1
         Ey_5 =  E_Array_y_n(x_i+1,y_j+1,z_k)*(p_i)*(p_j)*(1-p_k); % 1 1 0
         Ey_6 =  E_Array_y_n(x_i+1,y_j,z_k+1)*(p_i)*(1-p_j)*(p_k); % 1 0 1
         Ey_7 =   E_Array_y_n(x_i,y_j+1,z_k+1)*(1-p_i)*(p_j)*(p_k); % 0 1 1
         Ey_8 =  E_Array_y_n(x_i+1,y_j+1,z_k+1)*(p_i)*(p_j)*(p_k); % 1 1 1 
%         
        Ez_1 =  E_Array_z_n(x_i,y_j,z_k)*(1-p_i) *(1-p_j)*(1-p_k);  % 0 0 0
         Ez_2 = E_Array_z_n(x_i,y_j+1,z_k)*(1-p_i)*(p_j)*(1-p_k); %0 1 0
         Ez_3 = E_Array_z_n(x_i+1,y_j,z_k)*(p_i)*(1-p_j)*(1-p_k); %1 0 0
         Ez_4 = E_Array_z_n(x_i,y_j,z_k+1)*(1-p_i)*(1-p_j)*(p_k); %0 0 1
         Ez_5 =  E_Array_z_n(x_i+1,y_j+1,z_k)*(p_i)*(p_j)*(1-p_k); % 1 1 0
         Ez_6 =  E_Array_z_n(x_i+1,y_j,z_k+1)*(p_i)*(1-p_j)*(p_k); % 1 0 1
         Ez_7 =   E_Array_z_n(x_i,y_j+1,z_k+1)*(1-p_i)*(p_j)*(p_k); % 0 1 1
         Ez_8 =  E_Array_z_n(x_i+1,y_j+1,z_k+1)*(p_i)*(p_j)*(p_k); % 1 1 1
         
         
         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
         Bx_1 =  B_Array_x_n(x_i,y_j,z_k)*(1-p_i) *(1-p_j)*(1-p_k);  % 0 0 0
         Bx_2 = B_Array_x_n(x_i,y_j+1,z_k)*(1-p_i)*(p_j)*(1-p_k); %0 1 0
         Bx_3 = B_Array_x_n(x_i+1,y_j,z_k)*(p_i)*(1-p_j)*(1-p_k); %1 0 0
         Bx_4 = B_Array_x_n(x_i,y_j,z_k+1)*(1-p_i)*(1-p_j)*(p_k); %0 0 1
         Bx_5 =  B_Array_x_n(x_i+1,y_j+1,z_k)*(p_i)*(p_j)*(1-p_k); % 1 1 0
         Bx_6 =  B_Array_x_n(x_i+1,y_j,z_k+1)*(p_i)*(1-p_j)*(p_k); % 1 0 1
         Bx_7 =   B_Array_x_n(x_i,y_j+1,z_k+1)*(1-p_i)*(p_j)*(p_k); % 0 1 1
         Bx_8 =  B_Array_x_n(x_i+1,y_j+1,z_k+1)*(p_i)*(p_j)*(p_k); % 1 1 1 
         
        By_1 =  B_Array_y_n(x_i,y_j,z_k)*(1-p_i) *(1-p_j)*(1-p_k);  % 0 0 0
         By_2 = B_Array_y_n(x_i,y_j+1,z_k)*(1-p_i)*(p_j)*(1-p_k); %0 1 0
         By_3 = B_Array_y_n(x_i+1,y_j,z_k)*(p_i)*(1-p_j)*(1-p_k); %1 0 0
         By_4 = B_Array_y_n(x_i,y_j,z_k+1)*(1-p_i)*(1-p_j)*(p_k); %0 0 1
         By_5 =  B_Array_y_n(x_i+1,y_j+1,z_k)*(p_i)*(p_j)*(1-p_k); % 1 1 0
         By_6 =  B_Array_y_n(x_i+1,y_j,z_k+1)*(p_i)*(1-p_j)*(p_k); % 1 0 1
         By_7 =   B_Array_y_n(x_i,y_j+1,z_k+1)*(1-p_i)*(p_j)*(p_k); % 0 1 1
         By_8 =  B_Array_y_n(x_i+1,y_j+1,z_k+1)*(p_i)*(p_j)*(p_k); % 1 1 1 
         
         Bz_1 =  B_Array_z_n(x_i,y_j,z_k)*(1-p_i) *(1-p_j)*(1-p_k);  % 0 0 0
         Bz_2 = B_Array_z_n(x_i,y_j+1,z_k)*(1-p_i)*(p_j)*(1-p_k); %0 1 0
         Bz_3 = B_Array_z_n(x_i+1,y_j,z_k)*(p_i)*(1-p_j)*(1-p_k); %1 0 0
         Bz_4 = B_Array_z_n(x_i,y_j,z_k+1)*(1-p_i)*(1-p_j)*(p_k); %0 0 1
         Bz_5 =  B_Array_z_n(x_i+1,y_j+1,z_k)*(p_i)*(p_j)*(1-p_k); % 1 1 0
         Bz_6 =  B_Array_z_n(x_i+1,y_j,z_k+1)*(p_i)*(1-p_j)*(p_k); % 1 0 1
         Bz_7 =   B_Array_z_n(x_i,y_j+1,z_k+1)*(1-p_i)*(p_j)*(p_k); % 0 1 1
         Bz_8 =  B_Array_z_n(x_i+1,y_j+1,z_k+1)*(p_i)*(p_j)*(p_k); % 1 1 1 
%         
        

   else
       Ex_1=0;Ex_2=0;Ex_3=0;Ex_4=0;Ex_5=0;Ex_6=0;Ex_7=0;Ex_8=0; 
       Ey_1=0;Ey_2=0;Ey_3=0;Ey_4=0;Ey_5=0;Ey_6=0;Ey_7=0;Ey_8=0;
       Ez_1=0;Ez_2=0;Ez_3=0;Ez_4=0;Ez_5=0;Ez_6=0;Ez_7=0;Ez_8=0;
       
       
       Bx_1=0;Bx_2=0;Bx_3=0;Bx_4=0;Bx_5=0;Bx_6=0;Bx_7=0;Bx_8=0; 
       By_1=0;By_2=0;By_3=0;By_4=0;By_5=0;By_6=0;By_7=0;By_8=0;
       Bz_1=0;Bz_2=0;Bz_3=0;Bz_4=0;Bz_5=0;Bz_6=0;Bz_7=0;Bz_8=0;
       
    end 
       ExP_tt= Ex_1 + Ex_2 + Ex_3 +Ex_4 + Ex_5 + Ex_6 + Ex_7 + Ex_8;
       EyP_tt = Ey_1 + Ey_2 + Ey_3 +Ey_4 + Ey_5 + Ey_6 + Ey_7 + Ey_8;
       EzP_tt = Ez_1 + Ez_2 + Ez_3 +Ez_4 + Ez_5 + Ez_6 + Ez_7 + Ez_8;
       
       BxP_tt = Bx_1 + Bx_2 + Bx_3 +Bx_4 + Bx_5 + Bx_6 +Bx_7 + Bx_8;
       ByP_tt = By_1 + By_2 + By_3 +By_4 + By_5 + By_6 + By_7 + By_8;
       BzP_tt = Bz_1 + Bz_2 + Bz_3 +Bz_4 + Bz_5 + Bz_6 + Bz_7 + Bz_8;
       
       
       E_Field_At_Particle = [ExP_tt; EyP_tt; EzP_tt];
       B_Field_At_Particle = [BxP_tt; ByP_tt; BzP_tt];
       
end
