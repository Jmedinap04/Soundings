# Atmospheric Radiosonde Data Analysis with Python

This repository provides a comprehensive suite of Python tools for downloading, processing, and analyzing atmospheric radiosonde data. It consists of two primary components: a Python script for downloading ERA5 reanalysis data and a Jupyter Notebook for comprehensive thermodynamic analysis of atmospheric soundings.

## Overview

The package enables researchers to perform detailed atmospheric analysis using both observational radiosonde data and ERA5 reanalysis data. It provides capabilities for thermodynamic calculations, Skew-T log-P diagram visualization, and comprehensive atmospheric stability analysis.

## Requirements

- Python 3.x
- Core dependencies: `numpy`, `pandas`, `matplotlib`
- Atmospheric data libraries: `sounderpy`, `metpy`
- API access: [CDS API](https://cds.climate.copernicus.eu/api-how-to) for ERA5 data

Install dependencies using:

```bash
pip install numpy pandas matplotlib sounderpy metpy
pip install cdsapi
```

## Table of Contents

- [Installation](#installation)
- [ERA5 Data Download Script](#era5-data-download-script)
- [Radiosonde Analysis Notebook](#radiosonde-analysis-notebook)
- [Thermodynamic Calculations](#thermodynamic-calculations)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)

## Installation

### Prerequisites

The analysis tools require Python 3.x and the installation of several scientific computing packages. The system is designed for atmospheric research applications, particularly LIDAR signal analysis.

### Copernicus Climate Data Store (CDS) API Configuration

To download ERA5 reanalysis data, you must configure access to the Copernicus Climate Data Store:

1. **Create an account** at [https://cds.climate.copernicus.eu/](https://cds.climate.copernicus.eu/)

2. **Obtain your API key** by accessing your profile at [https://cds.climate.copernicus.eu/user](https://cds.climate.copernicus.eu/user)

3. **Create the `.cdsapirc` configuration file** in your home directory:

   Linux/macOS:
   ```bash
   ~/.cdsapirc
   ```

   Windows:
   ```bash
   C:\Users\Username\.cdsapirc
   ```

   File content format:
   ```
   url: https://cds.climate.copernicus.eu/api/v2
   key: YOUR-UID:YOUR-API-KEY
   ```

4. **Install the CDS API client**:
   ```bash
   pip install cdsapi
   ```

## ERA5 Data Download Script

### Overview

The `downloadSounding.py` script enables automated download of atmospheric profiles from ERA5 reanalysis data. It provides height, pressure, and temperature profiles for specified coordinates and temporal parameters, with optional vertical resolution resampling optimized for LIDAR analysis applications.

### Key Features

- Global coverage using ERA5 reanalysis data (0.25° resolution)
- Configurable vertical resolution for LIDAR applications
- CSV output format for data portability
- Command-line interface with fallback to hardcoded parameters

### Usage

The script can be executed with command-line arguments or using predefined parameters:

```bash
python downloadSounding.py latitude longitude resolution date hour output_folder
```

**Parameter specifications:**
- `latitude`: Decimal degrees (-90 to 90)
- `longitude`: Decimal degrees (-180 to 180)
- `resolution`: Vertical resolution in meters (use negative values for native 250m resolution)
- `date`: Date in 'YYYY-MM-DD' format
- `hour`: Hour in 'HH' format (UTC)
- `output_folder`: Directory for saved data files

**Example:**
```bash
python downloadSounding.py 40.0 -3.7 3.75 2024-07-15 12 Madrid_Soundings
```

## Radiosonde Analysis Notebook

### Overview

The `analisis_sondeo.ipynb` notebook provides comprehensive tools for atmospheric sounding analysis, including observational data acquisition, thermodynamic calculations, and atmospheric stability assessment.

### Core Functionality

#### 1. Observational Data Acquisition

The notebook supports downloading radiosonde data from multiple sources:
- **RAOB**: National Weather Service radiosonde observations
- **IGRAv2**: Integrated Global Radiosonde Archive

Supported Spanish meteorological stations include:
- Madrid/Barajas (08221/LEMD)
- Granada (08419)
- Barcelona (08190)
- La Coruña (08002/LECO)
- And 15+ additional stations

#### 2. Data Interpolation and Processing

The system provides flexible data interpolation capabilities:
- **Pressure-based interpolation**: Configurable resolution in hPa
- **Height-based interpolation**: Configurable resolution in meters
- **Quality control**: Automatic data validation and error handling

#### 3. Thermodynamic Analysis

Comprehensive calculation of atmospheric parameters:

**Basic Parameters:**
- Potential temperature (θ)
- Mixing ratio (r)
- Vapor pressure (e)
- Relative humidity (U)

**Advanced Thermodynamic Variables:**
- Lifting Condensation Level (LCL/NCE)
- Level of Free Convection (LFC/NCL)
- Equilibrium Level (EL/NCC)
- Wet-bulb temperature (T_sw)
- Equivalent potential temperature (θ_se)
- Pseudoequivalent temperature (T_se)

#### 4. Convective Parameters

**Stability Indices:**
- Convective Available Potential Energy (CAPE)
- Convective Inhibition (CIN)
- Convection temperature (T_conv)

#### 5. Visualization

**Skew-T Log-P Diagrams:**
- Temperature and dewpoint profiles
- Dry and moist adiabats
- Mixing ratio lines
- Parcel trajectories
- Stability area shading (CAPE/CIN)

**Customizable Display Options:**
- Adjustable pressure and temperature ranges
- Optional isotherms and isobars
- Multiple data overlay capabilities
- High-resolution output for publications

## Thermodynamic Calculations

### Fundamental Equations

The notebook implements standard atmospheric thermodynamic relationships:

1. **Potential Temperature**: θ = T(1000/P)^(R/cp)
2. **Mixing Ratio**: r = ε(e/(P-e))
3. **Equivalent Potential Temperature**: θ_e = θ * exp((L_v * r)/(c_p * T))
4. **Wet Bulb Temperature**: Calculated via iterative psychrometric methods

### Stability Analysis

The system provides comprehensive convective stability assessment through:
- **Parcel method analysis**: Following air parcel trajectories
- **Energy calculation**: CAPE and CIN integration
- **Critical level identification**: LCL, LFC, and EL detection

## Usage Examples

### Basic Analysis Workflow

1. **Data Acquisition**:
   ```python
   site_id = 'SPM00008221'  # Madrid/Barajas
   year, month, day, hour = '2022', '05', '20', '12'
   obs_data = spy.get_obs_data(site_id, year, month, day, hour)
   ```

2. **Data Processing**:
   ```python
   # Interpolate to desired resolution
   obs_data_interp = interpolar_radiosondeo(df_data, metodo='presion', resolucion=20)
   ```

3. **Thermodynamic Analysis**:
   ```python
   # Calculate LCL
   lcl_pressure, lcl_temperature = mpcalc.lcl(P[0], T[0], Td[0])
   
   # Calculate CAPE and CIN
   cape, cin = mpcalc.cape_cin(P, T, Td, parcel_profile)
   ```

4. **Visualization**:
   ```python
   # Create Skew-T diagram
   skew = SkewT(rotation=45)
   skew.plot(P, T, 'red', label='Temperature')
   skew.plot(P, Td, 'blue', label='Dewpoint')
   ```

## Configuration

### Key Parameters

**Data Resolution:**
- `dz`: Vertical resolution in meters (default: 10m)
- `dp`: Pressure resolution in hPa (default: 20 hPa)

**Visualization:**
- `p_min`, `p_max`: Pressure axis limits
- `T_min`, `T_max`: Temperature axis limits
- `save_img`: Enable/disable figure saving

**Analysis Options:**
- `usar_interpolado`: Use interpolated vs. original data
- `get_Td`: Include dewpoint temperature analysis
- `int_presion`/`int_altura`: Interpolation method selection

## Output Files

The system generates multiple output formats:
- **CSV files**: Raw and processed sounding data
- **PNG images**: High-resolution Skew-T diagrams
- **Analysis reports**: Thermodynamic parameter summaries

## Applications

This toolset is particularly suited for:
- **LIDAR atmospheric analysis**: Optimized vertical resolution matching
- **Meteorological research**: Comprehensive stability assessment
- **Climate studies**: Long-term atmospheric trend analysis
- **Educational purposes**: Interactive thermodynamic exploration

## Technical Notes

- **Data Quality**: Automatic handling of missing or erroneous observations
- **Performance**: Optimized for large datasets with efficient interpolation algorithms
- **Compatibility**: Cross-platform support (Linux, Windows, macOS)
- **Extensibility**: Modular design for custom analysis implementations

## File Structure

```
├── downloadSounding.py          # ERA5 data download script
├── analisis_sondeo.ipynb       # Comprehensive analysis notebook
├── funciones.py                # Interpolation utility functions
└── README.md                   # This documentation
```

## Citation

If you use this software in your research, please cite the original SounderPy library by Kyle J. Gillett and acknowledge the ERA5 reanalysis data from the Copernicus Climate Change Service.

## License

This project is distributed under standard academic use terms. Please refer to the LICENSE file for detailed information.
