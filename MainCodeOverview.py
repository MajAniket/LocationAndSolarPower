import pandas as pd
import pvlib

# Define location
# 42.37136, -72.638162 (Farm in West Hatfield, MA)
lat = 42.37136
lon = -72.638162

# Define time range
start = pd.Timestamp('2023-06-01', tz='America/New_York')
end = pd.Timestamp('2023-08-31', tz='America/New_York')
time_range = pd.date_range(start=start, end=end, freq='D', tz='America/New_York')

# Get solar position
solar_position = pvlib.solarposition.get_solarposition(time_range, lat, lon)

# Get extraterrestrial radiation
dni_extra = pvlib.irradiance.get_extra_radiation(time_range)

# Get atmospheric conditions
pressure = pvlib.atmosphere.alt2pres(0)
airmass = pvlib.atmosphere.get_relative_airmass(solar_position['apparent_zenith'])
extinction = pvlib.atmosphere.get_total_irradiance(airmass, pressure)

# Calculate irradiance
dni = pvlib.irradiance.dirint(dni_extra, solar_position['apparent_zenith'])
dhi = pvlib.irradiance.haydavies(solar_position['apparent_zenith'], extinction['h2o'], pressure)
ghi = pvlib.irradiance.globalinplane(dni, dhi, solar_position['apparent_zenith'], 0)

# Calculate energy production
system = {'module_parameters': {'pdc0': 300}, 'inverter_parameters': {'pdc0
