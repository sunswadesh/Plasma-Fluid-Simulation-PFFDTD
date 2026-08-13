% Function to perform Boris Particle Push
% q,m,dt are scalars
% V_prev_half_step, E_field, B_field are vectors in 3-D size (3,1)

function V_next_half_step = boris_push0(q, m, dt, V_prev_half_step, E_field, B_field)

V_next_half_step = zeros(3,1);

% Step 1 Calculate intermediate variable V_minus

V_minus = V_prev_half_step + (q*dt/2/m)*E_field;

% Calculate T vector, S_vector, V_prime, and V_plus

T_vector = (q*dt/m/2)*B_field;
S_vector = 2*T_vector/(1+T_vector'*T_vector);

V_prime = V_minus + cross(V_minus,T_vector);
V_plus  = V_minus + cross(V_prime,S_vector);

% Calculate V_next_half_step and return to calling function

V_next_half_step = V_plus + (q*dt/2/m)*E_field;

end
