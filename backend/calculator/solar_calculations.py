# backend/calculator/solar_calculations.py

from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['POST'])
def calculate_solar_setup(request):
    data = request.data
    power_consumption = data.get('powerConsumption', 0)  # in Watts
    backup_time = data.get('backupTime', 0)  # in hours
    sunlight_factor = data.get('sunlightFactor', 1.5)  # based on area
    panel_watt_choice = data.get('panelWattChoice', 180)  # single panel wattage
    battery_type = data.get('batteryType', 'leadAcid')  # battery type

    # Step 2: Inverter Selection
    recommended_inverter_watt = max(800, power_consumption * 1.2)  # at least 20% above the load

    # Step 3: Battery Size Calculation
    battery_capacity = (power_consumption * backup_time) / 12  # in Ah
    rounded_battery_capacity = round(battery_capacity / 50) * 50  # rounding to nearest standard (e.g., 250 Ah)

    # Calculate battery charging current
    battery_charging_current = rounded_battery_capacity * 0.1  # 10% of Ah rating

    # Step 4: Solar Panel Selection
    home_load_current = power_consumption / 12  # I = P / V, assuming 12V
    solar_plate_current = battery_charging_current + home_load_current
    total_solar_panel_power = 12 * solar_plate_current  # P = V * I

    # Calculate the number of solar plates
    num_solar_panels = round(total_solar_panel_power / panel_watt_choice)

    # Approximate costs (example values for Rs)
    battery_cost = 15000 if battery_type == 'leadAcid' else 30000  # assume 15000 for lead acid, 30000 for lithium
    inverter_cost = 50000  # assumed cost for inverter
    solar_panel_cost = num_solar_panels * 5000  # assume 5000 per panel

    # Total budget estimate
    total_budget = battery_cost + inverter_cost + solar_panel_cost

    # Return the results
    return JsonResponse({
        'recommendedInverterWatt': recommended_inverter_watt,
        'batteryCapacityAh': rounded_battery_capacity,
        'batteryChargingCurrent': battery_charging_current,
        'totalSolarPanelPower': total_solar_panel_power,
        'numSolarPanels': num_solar_panels,
        'totalBudget': total_budget,
        'batteryCost': battery_cost,
        'inverterCost': inverter_cost,
        'solarPanelCost': solar_panel_cost
    })
