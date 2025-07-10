import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def interpolate_dz(df, dz=10):
    """
    Interpola los datos del radiosondeo en función de la altura con una resolución vertical específica.
    
    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con columnas 'z' (altura en m), 'T' (temperatura en °C), 
        'p' (presión en hPa), y 'Td' (temperatura de rocío en °C)
    dz : float, opcional
        Resolución vertical en metros (por defecto 10 m)
    
    Retorna:
    --------
    pd.DataFrame
        DataFrame interpolado con la resolución vertical especificada
    """
    # Asegurar que los datos estén ordenados por altura ascendente
    df = df.sort_values('z', ascending=True).reset_index(drop=True)
    
    # Crear el nuevo eje de altura con la resolución deseada
    z_min, z_max = df['z'].min(), df['z'].max()
    z_nuevo = np.arange(z_min, z_max + dz, dz)
    
    # Crear funciones de interpolación para cada variable
    interp_T = interp1d(df['z'], df['T'], bounds_error=False, fill_value='extrapolate')
    interp_p = interp1d(df['z'], df['p'], bounds_error=False, fill_value='extrapolate')
    interp_Td = interp1d(df['z'], df['Td'], bounds_error=False, fill_value='extrapolate')
    
    # Aplicar interpolación
    T_nueva = interp_T(z_nuevo)
    p_nueva = interp_p(z_nuevo)
    Td_nueva = interp_Td(z_nuevo)
    
    # Crear nuevo DataFrame
    df_interp = pd.DataFrame({
        'z': z_nuevo,
        'T': T_nueva,
        'p': p_nueva,
        'Td': Td_nueva
    })
    
    return df_interp

def interpolate_dp(df, dp=1):
    """
    Interpola los datos del radiosondeo en función de la presión con una resolución específica.
    
    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con columnas 'z' (altura en m), 'T' (temperatura en °C), 
        'p' (presión en hPa), y 'Td' (temperatura de rocío en °C)
    dp : float, opcional
        Resolución de presión en hPa (por defecto 1 hPa)
    
    Retorna:
    --------
    pd.DataFrame
        DataFrame interpolado con la resolución de presión especificada
    """
    # Asegurar que los datos estén ordenados por presión descendente (como en los sondeos reales)
    df = df.sort_values('p', ascending=False).reset_index(drop=True)
    
    # Crear un nuevo eje de presión con la resolución deseada
    p_min, p_max = df['p'].min(), df['p'].max()
    p_nuevo = np.arange(p_max, p_min - dp, -dp)
    
    # Crear funciones de interpolación para cada variable
    interp_T = interp1d(df['p'], df['T'], bounds_error=False, fill_value='extrapolate')
    interp_z = interp1d(df['p'], df['z'], bounds_error=False, fill_value='extrapolate')
    interp_Td = interp1d(df['p'], df['Td'], bounds_error=False, fill_value='extrapolate')
    
    # Aplicar interpolación
    T_nueva = interp_T(p_nuevo)
    z_nueva = interp_z(p_nuevo)
    Td_nueva = interp_Td(p_nuevo)
    
    # Crear nuevo DataFrame
    df_interp = pd.DataFrame({
        'p': p_nuevo,
        'T': T_nueva,
        'z': z_nueva,
        'Td': Td_nueva
    })
    
    return df_interp

def interpolar_radiosondeo(df, metodo='presion', resolucion=None):
    """
    Función general para interpolar datos de radiosondeo.
    
    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con columnas 'z', 'T', 'p', 'Td'
    metodo : str
        'presion' para interpolación por presión o 'altura' para interpolación por altura
    resolucion : float
        Resolución deseada (hPa para presión, m para altura)
    
    Retorna:
    --------
    pd.DataFrame
        DataFrame interpolado
    """
    if metodo.lower() == 'presion':
        dp = resolucion if resolucion is not None else 1
        return interpolate_dp(df, dp)
    elif metodo.lower() == 'altura':
        dz = resolucion if resolucion is not None else 10
        return interpolate_dz(df, dz)
    else:
        raise ValueError("El método debe ser 'presion' o 'altura'")

# # Ejemplo de uso de las funciones:
# print("Funciones de interpolación definidas:")
# print("- interpolate_dz(df, dz=10): Interpola por altura")
# print("- interpolate_dp(df, dp=1): Interpola por presión") 
# print("- interpolar_radiosondeo(df, metodo='presion'|'altura', resolucion=valor): Función general")
