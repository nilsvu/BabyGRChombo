# mymatter.py
# Calculates the matter rhs and stress energy contributions
# this assumes spherical symmetry

import numpy as np
from myparams import *
from source.tensoralgebra import *

def get_matter_rhs(u, v, dudr, d2udx2, bar_gamma_UU, em4phi, dphidr, K, lapse, dlapsedr) :
    dudt =  lapse * v
    dvdt =  lapse * K * v + bar_gamma_UU[i_r][i_r] * em4phi * (2.0 * lapse * dphidr * dudr 
                                                               + lapse * d2udx2 + 0.0 * dlapsedr * dudr)
    
    # Add mass term
    dVdu = scalar_mu * scalar_mu * u
    dvdt += - lapse * dVdu
    
    return dudt, dvdt

def get_rho(u, dudr, v, bar_gamma_UU, em4phi) :

    # The potential V(u) = 1/2 mu^2 u^2
    V_u = 0.5 * scalar_mu * scalar_mu * u * u
    rho = 0.5 * v*v + 0.5 * em4phi * bar_gamma_UU[i_r][i_r] * dudr * dudr + V_u

    return rho

def get_Si(u, dudr, v, bar_gamma_UU, em4phi) :
    S_i = np.zeros_like(rank_1_spatial_tensor)
    
    S_i[i_r] = - v * dudr
    
    return S_i

def get_Sij(u, dudr, v, bar_gamma_UU, em4phi, bar_gamma_LL) :
    S_ij = np.zeros_like(rank_2_spatial_tensor)

    # The potential V(u) = 1/2 mu^2 u^2
    V_u = 0.5 * scalar_mu * scalar_mu * u * u
    
    # Useful quantity Vt
    Vt = - v*v + em4phi * bar_gamma_UU[i_r][i_r] * (dudr * dudr)
    for i in range(0, SPACEDIM):    
        S_ij[i][i] = - (0.5 * Vt  + V_u) * bar_gamma_LL[i][i] / em4phi + delta[i][i_r] * dudr * dudr
    
    # The trace of S_ij
    S = 0.0
    for i in range(0, SPACEDIM): 
        for j in range(0, SPACEDIM):
            S += S_ij[i][j] * bar_gamma_UU[i][j] * em4phi
    return S, S_ij
