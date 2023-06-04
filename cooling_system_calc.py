import math
import numpy as np

# upload to fsae git

# Links
# Measure Instructions: https://www.maplesoft.com/support/help/maple/view.aspx?path=applications/RadiatorDesign 

# Inputs
system_types = {
    "single": "Single heat exchanger",
    "series": "Series same size heat exchangers",
    "parallel": "Parallel same size heat exchangers"
}
selected_system_type = "parallel" 
length = .75 # ft
width = .75 # ft
depth = .132625 # ft
tube_width = depth 
tube_height = .0065 # ft
fin_width = depth
fin_height = .02125  # ft
fin_thickness = .0005  # ft
distance_between_fins = .00225  # ft
number_of_tubes = math.floor(width / (tube_height + fin_height))
number_of_air_passages = math.floor(length * number_of_tubes / (distance_between_fins + fin_thickness))
coolant_volumetric_flow = 14 # gpm # across radiator not at pump
air_volumetric_flow = (0.29 * 9 * 9 / (9 * 12)) * 2119 # ft^3/min converted from m^3/s ### Verify this value
air_velocity = 25  # mph ## convert to velocity air and below
coolant_temperature = 200 # F
air_temperature = 80 # F
time_averaged_engine_power_output = 75 # hp  #### To change
q_oil_cooler = 32000 # btu/hr
length_connecting_tubes = 5 # ft

# Constants
thermal_conductivity_water = 0.35  # Btu/h(ft)F
specific_heat_water = 1  # Btu/lbF
density_water = 62  # lb/ft^3
dynamic_viscosity_water = 0.0002041  # lb/fts
thermal_conductivity_air = 0.0154  # Btu/h(ft)F
specific_heat_air = 0.24  # Btu/lbF
density_air = 0.071  # lb/ft^3
dynamic_viscosity_air = 0.00001285  # lb/fts

## Calculated Values
# Area Calculations
coolant_area = 2 * number_of_tubes * ((length * tube_width) + (length * tube_height)) # (ft^2)
air_area = 2 * number_of_air_passages * ((fin_width * fin_height) + (fin_height * distance_between_fins)) # (ft^2)
total_area = coolant_area + air_area # (ft^2)

# Performance Calculations for Coolant
min_area_coolant = tube_width * tube_height # (ft^2)
wetted_perimeter = 2 * (tube_width + tube_height) # (ft)
hydraulic_diameter = 4 * min_area_coolant / wetted_perimeter # (ft)
velocity_water = (coolant_volumetric_flow / number_of_tubes / min_area_coolant) * 0.133681 / 60 # (ft/sec)
reynolds_number_water = (density_water * velocity_water * hydraulic_diameter) / dynamic_viscosity_water # 
prandt_number_water = (specific_heat_water * (dynamic_viscosity_water / thermal_conductivity_water)) * 3600 # 
nusselt_number_water = 0.023 * (reynolds_number_water ** 0.8) * (prandt_number_water ** (1/3)) # 
hc_water = nusselt_number_water * thermal_conductivity_water / hydraulic_diameter # (Btu/h(ft^2)F)
mass_flow_rate_water = (coolant_volumetric_flow * density_water / 60) * 0.133681 # (lb/sec)
thermal_capacity_rate_water = mass_flow_rate_water * specific_heat_water * 60 # (Btu/minF)

# Performance Calculations for Air
min_area_air = fin_height * distance_between_fins # (ft^2)
wetted_perimeter_air = 2 * (distance_between_fins + (8 * distance_between_fins)) # (ft)
hydraulic_diameter_air = 4 * min_area_air / wetted_perimeter_air # (ft)
reynolds_number_air = (density_air * air_velocity * hydraulic_diameter_air) / dynamic_viscosity_air * 5280 / 3600 # 
mass_flow_rate_air = (air_volumetric_flow * density_air) / 60 # (lb/sec)
thermal_capacity_rate_air = mass_flow_rate_air * specific_heat_air * 60 # (Btu/minF)

# Performance Calculations for single radiator
thermal_capacity_rate_min = min(thermal_capacity_rate_air, thermal_capacity_rate_water)
thermal_capacity_rate_max = max(thermal_capacity_rate_air, thermal_capacity_rate_water)
thermal_capacity_ratio = thermal_capacity_rate_air / thermal_capacity_rate_water
idt = coolant_temperature - air_temperature # (F)
nfha = 47.0113
universal_heat_transfer_coefficient = ((1 / (hc_water * coolant_area) * 60) + (1 / (nfha * air_area) * 60)) ** (-1) # (btu/minF)
Ntu = universal_heat_transfer_coefficient / thermal_capacity_rate_min ############
effectiveness = 1 - math.exp(-(thermal_capacity_rate_max * (1 - math.exp(-thermal_capacity_ratio * Ntu))) / thermal_capacity_rate_min)

# Oil cooler
q_oil_cooler = q_oil_cooler / 60 # btu/min

# Amount of Heat Produced by Engine
approx_heat_production = time_averaged_engine_power_output / 3 * 42.40717 # (Btu/min)
heat_to_be_removed_by_radiator = approx_heat_production - q_oil_cooler # (Btu/min)

volume_water_connecting_tubes = np.pi * (1/12)**(2) * length_connecting_tubes # (ft^3)
#mass water =? lbs

if selected_system_type == "single":
    number_of_heat_exchangers = 1
elif selected_system_type == "series":
    number_of_heat_exchangers = 2
elif selected_system_type == "parallel":
    number_of_heat_exchangers = 2

def calculate_single_results():
    # Add equations and calculations for a single heat exchanger
    q_radiator = effectiveness * thermal_capacity_rate_min * idt # (Btu/min)
    final_temp = coolant_temperature - (q_radiator / (mass_flow_rate_water * 60 * specific_heat_air)) # (F)
    total_deltaT_for_radiator = coolant_temperature - (q_radiator / (mass_flow_rate_water * 60 * specific_heat_air)) # (F)
    change_in_temperature = approx_heat_production / (mass_flow_rate_water * 60 * specific_heat_air) # (F)
    total_heat_removed = q_radiator * number_of_heat_exchangers # (Btu/min)
    Thermal_FOS = q_radiator / approx_heat_production
    
    # Print single results
    print(f"Radiator Heat Transfer: {q_radiator:.2f} Btu/min")
    print(f"Final Temperature: {final_temp:.2f} F")
    print(f"Total Delta T for Radiator: {total_deltaT_for_radiator:.2f} F")
    print(f"Total Heat Removed: {total_heat_removed:.2f} Btu/min")
    print(f"Change in Temperature: {change_in_temperature:.2f} F")
    print(f"Series Thermal FOS: {Thermal_FOS:.2f}")
    pass

def calculate_series_results():
    q_radiator = effectiveness * thermal_capacity_rate_min * idt # (Btu/min)
    intermediate_temp = coolant_temperature - (q_radiator / (mass_flow_rate_water * 60 * specific_heat_air)) # (F)
    idt_second_radiator_ = intermediate_temp - air_temperature # (F) ######## 2 idts
    q_second_radiator = idt_second_radiator_ * thermal_capacity_rate_min * effectiveness # (Btu/min)
    final_temp = intermediate_temp - (q_second_radiator / (mass_flow_rate_water * 60 * specific_heat_air)) # (F)
    total_heat_removed_series = q_radiator + q_second_radiator # (Btu/min)
    change_in_temperature = approx_heat_production / (mass_flow_rate_water * 60 * specific_heat_air) # (F)
    Thermal_FOS = total_heat_removed_series / approx_heat_production
    
    # print series results
    print(f"First Radiator Heat Trasnfer: {q_radiator:.2f} Btu/min")
    print(f"Intermediate Temp: {intermediate_temp} F")
    print(f"Intermediate Temperature Difference: {idt_second_radiator_} F")
    print(f"Second Radiator Heat Transfer: {q_second_radiator} Btu/min")
    print(f"Final Temp: {final_temp} F")
    print(f"Total Heat Rejection: {total_heat_removed_series} Btu/min")
    print(f"Change in Temperature: {change_in_temperature} F")
    print(f"Series Thermal FOS: {Thermal_FOS} F")
    pass

def calculate_parallel_results():
    # Important functions
    coolant_volumetric_flow_parallel = coolant_volumetric_flow / 2 # (ft^3/min)
    idt_parallel = idt
    
    velocity_water_parallel = (coolant_volumetric_flow_parallel / number_of_tubes / min_area_coolant) * 0.133681 / 60
    mass_flow_rate_water_parallel = (coolant_volumetric_flow_parallel * density_water / 60) * 0.133681 # (lb/sec)
    mass_flow_rate_air_parallel = (air_volumetric_flow * density_air) / 60 # (lb/sec)
    
    
    thermal_capacity_rate_water_parallel = mass_flow_rate_water_parallel * specific_heat_water * 60 # (Btu/minF)
    thermal_capacity_rate_air_parallel = mass_flow_rate_air_parallel * specific_heat_air * 60 # (Btu/minF)
    
    # Recalculate performance values for single radiator
    thermal_capacity_rate_min_parallel = min(thermal_capacity_rate_air_parallel, thermal_capacity_rate_water_parallel) # (Btu/minF)
    thermal_capacity_rate_max_parallel = max(thermal_capacity_rate_air_parallel, thermal_capacity_rate_water_parallel) # (Btu/minF)
    thermal_capacity_ratio_parallel = thermal_capacity_rate_air_parallel / thermal_capacity_rate_water_parallel # (Btu/minF)
    Ntu_parallel = universal_heat_transfer_coefficient / thermal_capacity_rate_min_parallel
    effectiveness_parallel = 1 - math.exp(-(thermal_capacity_rate_max_parallel * (1 - math.exp(-thermal_capacity_ratio_parallel * Ntu_parallel))) / thermal_capacity_rate_min_parallel) #
    
    # Calculate heat transfer and temperature for parallel radiators
    q_parallel_radiator = effectiveness_parallel * thermal_capacity_rate_min_parallel * idt_parallel # (Btu/min)
    final_temp_parallel = coolant_temperature - (q_parallel_radiator / (mass_flow_rate_water_parallel * 60 * specific_heat_air)) # (F)
    total_heat_removed_parallel = q_parallel_radiator * 2
    Thermal_FOS_parallel = total_heat_removed_parallel / approx_heat_production

    # Print parallel results
    print(f"Parallel Radiator Heat Transfer (each): {q_parallel_radiator} Btu/min")
    print(f"Final Temp: {final_temp_parallel} F")
    print(f"Total Heat Rejection: {total_heat_removed_parallel} Btu/min")
    print(f"Parallel Thermal FOS: {Thermal_FOS_parallel}")
pass

# Print results
print("\nArea Calculations:")
print(f"Coolant Area: {coolant_area:.2f} ft^2")
print(f"Air Area: {air_area:.2f} ft^2")
print(f"Total Area: {total_area:.2f} ft^2")
print("\nCoolant Calculations:")
print(f"Minimum Area Coolant: {min_area_coolant:.2f} ft^2")
print(f"Wetted Perimeter: {wetted_perimeter:.2f} ft")
print(f"Hydraulic Diameter: {hydraulic_diameter:.2f} ft")
print(f"Velocity Water: {velocity_water:.2f} ft/sec")
print(f"Reynolds Number Water: {reynolds_number_water:.2f}")
print(f"Prandt Number Water: {prandt_number_water:.2f}")
print(f"Nusselt Number Water: {nusselt_number_water:.2f}")
print(f"hc Water: {hc_water:.2f} Btu/h(ft^2)F")
print(f"Mass Flow Rate Water: {mass_flow_rate_water:.2f} lb/sec")
print(f"Thermal Capacity Rate Water: {thermal_capacity_rate_water:.2f} Btu/minF")
print(f"\nAir Calculations:")
print(f"Minimum Area Air: {min_area_air:.2f} ft^2")
print(f"Wetted Perimeter Air: {wetted_perimeter_air:.2f} ft")
print(f"Hydraulic Diameter Air: {hydraulic_diameter_air:.2f} ft")
print(f"Reynolds Number Air: {reynolds_number_air:.2f}")
print(f"Mass Flow Rate Air: {mass_flow_rate_air:.2f} lb/sec")
print(f"Thermal Capacity Rate Air: {thermal_capacity_rate_air:.2f} Btu/minF")
print(f"Calculated Values:")
print(f"Thermal Capacity Rate Min: {thermal_capacity_rate_min:.2f} Btu/minF")
print(f"Thermal Capacity Rate Max: {thermal_capacity_rate_max:.2f} Btu/minF")
print(f"Thermal Capacity Ratio: {thermal_capacity_ratio:.2f}")
print(f"Initial Temperature Difference: {idt:.2f} F")
print(f"nfha: {nfha:.2f}")
print(f"Universal Heat Transfer Coefficient: {universal_heat_transfer_coefficient:.2f} btu/minF")
print(f"Ntu: {Ntu:.2f}")
print(f"effectiveness: {effectiveness:.2f}")
print("\nAmount of Heat Produced by Engine:")
print(f"Time Averaged Engine Power Output: {time_averaged_engine_power_output:.2f} hp")
print(f"Approximate Heat Production: {approx_heat_production:.2f} Btu/min")

for current_system_type in system_types:
    if current_system_type == selected_system_type:
        print(f"\nResults for {system_types[selected_system_type]}:")

        if selected_system_type == "parallel":
            calculate_parallel_results()
        elif selected_system_type == "series":
            calculate_series_results()
        else:
            calculate_single_results()

        print("\n")  
   
## TO DO     
#plot volumetric flow rate vs. radiator frontal area
# table number of rads etc.
# mass flowrate needed at 100degf
#calculate miniumm surface area of radiator
#performance maps where heat exchanger performs across a range of operaing conditions. such as air flow rates and temperature changes
#calculating pressure drop across the heat exchanger/fan and provide that in calcs
#accomodate for mass of water in system
#include fan cfm and pressure drop        
#minimum surface area calculation


