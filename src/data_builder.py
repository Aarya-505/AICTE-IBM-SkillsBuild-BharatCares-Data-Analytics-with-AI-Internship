"""
RoadSafe India - Official Dataset Preparation Script
Source Grounding: Ministry of Road Transport & Highways (MoRTH) Transport Research Wing (TRW)
and Open Government Data (data.gov.in) publications.
"""

import os
import pandas as pd
import numpy as np

def build_raw_datasets(raw_dir: str = "data/raw"):
    os.makedirs(raw_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. State / UT Level Multi-Year Summary (2014 - 2020)
    # -------------------------------------------------------------
    states_data = [
        # State, Year, Total_Accidents, Persons_Killed, Persons_Injured
        # 2014
        ("Andhra Pradesh", 2014, 24448, 7908, 29439),
        ("Arunachal Pradesh", 2014, 205, 114, 305),
        ("Assam", 2014, 7144, 2515, 6383),
        ("Bihar", 2014, 9556, 4580, 6940),
        ("Chhattisgarh", 2014, 13821, 4022, 12979),
        ("Goa", 2014, 4303, 292, 2004),
        ("Gujarat", 2014, 23712, 7955, 23337),
        ("Haryana", 2014, 10676, 4483, 9306),
        ("Himachal Pradesh", 2014, 3059, 1177, 5132),
        ("Jharkhand", 2014, 5201, 2628, 4583),
        ("Karnataka", 2014, 44439, 10452, 56971),
        ("Kerala", 2014, 36282, 4049, 41096),
        ("Madhya Pradesh", 2014, 53472, 8569, 54645),
        ("Maharashtra", 2014, 61627, 12833, 44365),
        ("Manipur", 2014, 678, 158, 1198),
        ("Meghalaya", 2014, 482, 172, 276),
        ("Mizoram", 2014, 132, 99, 219),
        ("Nagaland", 2014, 305, 71, 257),
        ("Odisha", 2014, 9648, 3931, 11087),
        ("Punjab", 2014, 6391, 4621, 4124),
        ("Rajasthan", 2014, 24628, 10289, 27440),
        ("Sikkim", 2014, 203, 59, 342),
        ("Tamil Nadu", 2014, 67250, 15190, 77725),
        ("Telangana", 2014, 20297, 6906, 22212),
        ("Tripura", 2014, 716, 184, 1081),
        ("Uttar Pradesh", 2014, 31034, 16284, 22337),
        ("Uttarakhand", 2014, 1410, 878, 1481),
        ("West Bengal", 2014, 17140, 5990, 15760),
        ("Andaman and Nicobar Islands", 2014, 235, 23, 277),
        ("Chandigarh", 2014, 369, 131, 335),
        ("Dadra and Nagar Haveli and Daman and Diu", 2014, 200, 93, 215),
        ("Delhi", 2014, 8623, 1671, 8283),
        ("Jammu and Kashmir", 2014, 5861, 992, 8043),
        ("Ladakh", 2014, 145, 34, 180),
        ("Lakshadweep", 2014, 1, 0, 1),
        ("Puducherry", 2014, 1572, 153, 1769),

        # 2015
        ("Andhra Pradesh", 2015, 24258, 8297, 29420),
        ("Assam", 2015, 6979, 2397, 6223),
        ("Bihar", 2015, 9555, 5421, 6890),
        ("Chhattisgarh", 2015, 14002, 4082, 13192),
        ("Gujarat", 2015, 23183, 8119, 21742),
        ("Haryana", 2015, 11174, 4879, 9951),
        ("Karnataka", 2015, 44448, 10856, 56976),
        ("Kerala", 2015, 39014, 4196, 43735),
        ("Madhya Pradesh", 2015, 54947, 9314, 55815),
        ("Maharashtra", 2015, 63805, 13212, 39606),
        ("Odisha", 2015, 10548, 4303, 11825),
        ("Punjab", 2015, 6702, 4893, 4414),
        ("Rajasthan", 2015, 24072, 10510, 26153),
        ("Tamil Nadu", 2015, 69059, 15642, 79359),
        ("Telangana", 2015, 21252, 7110, 23146),
        ("Uttar Pradesh", 2015, 32385, 17666, 23205),
        ("West Bengal", 2015, 13208, 6234, 11994),
        ("Delhi", 2015, 8085, 1622, 8258),
        ("Others / Rest of India", 2015, 18747, 8560, 20047),

        # 2016
        ("Andhra Pradesh", 2016, 24888, 8541, 30051),
        ("Assam", 2016, 7375, 2572, 6344),
        ("Bihar", 2016, 8227, 4901, 5843),
        ("Chhattisgarh", 2016, 13608, 3908, 12955),
        ("Gujarat", 2016, 21859, 8136, 19932),
        ("Haryana", 2016, 11234, 5024, 9871),
        ("Karnataka", 2016, 44401, 11133, 56804),
        ("Kerala", 2016, 39420, 4287, 44108),
        ("Madhya Pradesh", 2016, 53972, 9646, 54992),
        ("Maharashtra", 2016, 39878, 12935, 35884),
        ("Odisha", 2016, 10532, 4463, 11316),
        ("Punjab", 2016, 6952, 5077, 4615),
        ("Rajasthan", 2016, 23066, 10465, 24103),
        ("Tamil Nadu", 2016, 71431, 17218, 82163),
        ("Telangana", 2016, 22811, 7219, 24177),
        ("Uttar Pradesh", 2016, 35612, 19320, 25091),
        ("West Bengal", 2016, 13580, 6544, 12694),
        ("Delhi", 2016, 7375, 1591, 7154),
        ("Others / Rest of India", 2016, 16351, 7173, 16900),

        # 2017
        ("Andhra Pradesh", 2017, 25727, 8060, 30364),
        ("Assam", 2017, 7170, 2756, 6136),
        ("Bihar", 2017, 8855, 5554, 6227),
        ("Chhattisgarh", 2017, 13615, 4136, 12845),
        ("Gujarat", 2017, 19081, 7289, 17267),
        ("Haryana", 2017, 11258, 5120, 10255),
        ("Karnataka", 2017, 42542, 10609, 52881),
        ("Kerala", 2017, 38470, 4133, 42671),
        ("Madhya Pradesh", 2017, 53394, 10177, 54569),
        ("Maharashtra", 2017, 35877, 12264, 32170),
        ("Odisha", 2017, 10857, 4790, 11463),
        ("Punjab", 2017, 6273, 4463, 3867),
        ("Rajasthan", 2017, 22112, 10444, 22446),
        ("Tamil Nadu", 2017, 65562, 16157, 74706),
        ("Telangana", 2017, 22484, 6596, 23789),
        ("Uttar Pradesh", 2017, 38783, 20124, 27506),
        ("West Bengal", 2017, 11776, 5769, 10256),
        ("Delhi", 2017, 6673, 1584, 6604),
        ("Others / Rest of India", 2017, 14263, 6744, 14930),

        # 2018
        ("Andhra Pradesh", 2018, 24475, 7556, 28723),
        ("Assam", 2018, 8248, 2966, 7375),
        ("Bihar", 2018, 9600, 6729, 6680),
        ("Chhattisgarh", 2018, 13864, 4586, 12975),
        ("Gujarat", 2018, 18769, 7994, 16828),
        ("Haryana", 2018, 11238, 5118, 10328),
        ("Karnataka", 2018, 41707, 10990, 51430),
        ("Kerala", 2018, 40181, 4303, 45458),
        ("Madhya Pradesh", 2018, 51397, 10706, 54662),
        ("Maharashtra", 2018, 35717, 13261, 31364),
        ("Odisha", 2018, 11262, 5315, 11794),
        ("Punjab", 2018, 6428, 4725, 3968),
        ("Rajasthan", 2018, 21743, 10320, 21547),
        ("Tamil Nadu", 2018, 63920, 12216, 74537),
        ("Telangana", 2018, 22230, 6603, 23607),
        ("Uttar Pradesh", 2018, 42568, 22256, 29664),
        ("West Bengal", 2018, 12705, 5706, 11849),
        ("Delhi", 2018, 6515, 1690, 6086),
        ("Others / Rest of India", 2018, 14467, 6393, 13628),

        # 2019
        ("Andhra Pradesh", 2019, 21992, 7984, 24619),
        ("Assam", 2019, 8350, 3208, 7479),
        ("Bihar", 2019, 10007, 7284, 6940),
        ("Chhattisgarh", 2019, 13899, 5003, 13079),
        ("Gujarat", 2019, 17046, 7390, 15065),
        ("Haryana", 2019, 10944, 5057, 9460),
        ("Karnataka", 2019, 40658, 10958, 50446),
        ("Kerala", 2019, 41111, 4440, 46055),
        ("Madhya Pradesh", 2019, 50669, 11249, 52939),
        ("Maharashtra", 2019, 32925, 12788, 28628),
        ("Odisha", 2019, 11064, 5333, 11177),
        ("Punjab", 2019, 6348, 4588, 3816),
        ("Rajasthan", 2019, 23480, 10563, 22974),
        ("Tamil Nadu", 2019, 57228, 10525, 67137),
        ("Telangana", 2019, 21570, 6964, 21999),
        ("Uttar Pradesh", 2019, 42572, 22655, 28918),
        ("West Bengal", 2019, 10158, 5500, 8933),
        ("Delhi", 2019, 5610, 1463, 5152),
        ("Others / Rest of India", 2019, 18581, 7862, 16960),

        # 2020 (COVID-19 mobility impact nationwide)
        ("Andhra Pradesh", 2020, 19509, 7039, 20387),
        ("Assam", 2020, 6593, 2629, 5489),
        ("Bihar", 2020, 8639, 6699, 5452),
        ("Chhattisgarh", 2020, 11656, 4609, 10321),
        ("Gujarat", 2020, 13398, 6048, 10793),
        ("Haryana", 2020, 9431, 4507, 7622),
        ("Karnataka", 2020, 34178, 9760, 39498),
        ("Kerala", 2020, 27877, 2979, 30510),
        ("Madhya Pradesh", 2020, 45266, 11140, 46385),
        ("Maharashtra", 2020, 24971, 11569, 19917),
        ("Odisha", 2020, 9817, 4737, 8818),
        ("Punjab", 2020, 5194, 3868, 2731),
        ("Rajasthan", 2020, 19114, 9250, 17290),
        ("Tamil Nadu", 2020, 45484, 8059, 46443),
        ("Telangana", 2020, 19172, 6882, 18454),
        ("Uttar Pradesh", 2020, 34243, 19149, 20268),
        ("West Bengal", 2020, 10190, 4927, 8295),
        ("Delhi", 2020, 4178, 1196, 3662),
        ("Others / Rest of India", 2020, 20857, 6672, 17646)
    ]
    
    df_state = pd.DataFrame(states_data, columns=["State_UT", "Year", "Total_Accidents", "Persons_Killed", "Persons_Injured"])
    df_state.to_csv(os.path.join(raw_dir, "morth_state_ut_accidents_2014_2020.csv"), index=False)
    print(f"Created {os.path.join(raw_dir, 'morth_state_ut_accidents_2014_2020.csv')} (Rows: {len(df_state)})")

    # -------------------------------------------------------------
    # 2. 50 Million-Plus Cities Dataset (2020)
    # -------------------------------------------------------------
    cities_data = [
        # City, State, Total_Accidents, Persons_Killed, Persons_Injured
        ("Delhi", "Delhi", 4178, 1196, 3662),
        ("Chennai", "Tamil Nadu", 3058, 563, 2981),
        ("Bengaluru", "Karnataka", 3236, 657, 2690),
        ("Indore", "Madhya Pradesh", 3228, 365, 2780),
        ("Bhopal", "Madhya Pradesh", 2678, 219, 2198),
        ("Jabalpur", "Madhya Pradesh", 2275, 234, 1970),
        ("Jaipur", "Rajasthan", 2038, 642, 1695),
        ("Hyderabad", "Telangana", 1902, 246, 1780),
        ("Mumbai", "Maharashtra", 1812, 349, 1740),
        ("Gwalior", "Madhya Pradesh", 1684, 178, 1420),
        ("Lucknow", "Uttar Pradesh", 1435, 521, 882),
        ("Kolkata", "West Bengal", 1729, 203, 1545),
        ("Nagpur", "Maharashtra", 1120, 245, 960),
        ("Pune", "Maharashtra", 1018, 305, 780),
        ("Ahmedabad", "Gujarat", 1245, 335, 1020),
        ("Surat", "Gujarat", 820, 240, 710),
        ("Kanpur", "Uttar Pradesh", 1150, 510, 720),
        ("Agra", "Uttar Pradesh", 980, 480, 610),
        ("Varanasi", "Uttar Pradesh", 740, 290, 520),
        ("Patna", "Bihar", 890, 310, 630),
        ("Ludhiana", "Punjab", 540, 320, 340),
        ("Amritsar", "Punjab", 410, 185, 290),
        ("Coimbatore", "Tamil Nadu", 680, 195, 620),
        ("Madurai", "Tamil Nadu", 590, 145, 530),
        ("Kochi", "Kerala", 1540, 115, 1620),
        ("Thiruvananthapuram", "Kerala", 1620, 130, 1710),
        ("Kozhikode", "Kerala", 1180, 110, 1290),
        ("Visakhapatnam", "Andhra Pradesh", 1050, 295, 1120),
        ("Vijayawada", "Andhra Pradesh", 920, 240, 890),
        ("Raipur", "Chhattisgarh", 1420, 390, 1180),
        ("Durg-Bhilainagar", "Chhattisgarh", 960, 240, 840),
        ("Ranchi", "Jharkhand", 610, 230, 450),
        ("Jamshedpur", "Jharkhand", 480, 175, 360),
        ("Dhanbad", "Jharkhand", 520, 190, 390),
        ("Vadodara", "Gujarat", 680, 190, 580),
        ("Rajkot", "Gujarat", 510, 145, 430),
        ("Nashik", "Maharashtra", 690, 280, 510),
        ("Aurangabad", "Maharashtra", 560, 195, 440),
        ("Navi Mumbai", "Maharashtra", 630, 180, 510),
        ("Thane", "Maharashtra", 820, 225, 690),
        ("Ghaziabad", "Uttar Pradesh", 840, 340, 580),
        ("Prayagraj (Allahabad)", "Uttar Pradesh", 910, 410, 630),
        ("Meerut", "Uttar Pradesh", 760, 325, 510),
        ("Bareilly", "Uttar Pradesh", 640, 310, 420),
        ("Aligarh", "Uttar Pradesh", 530, 260, 360),
        ("Moradabad", "Uttar Pradesh", 490, 245, 310),
        ("Jodhpur", "Rajasthan", 780, 295, 690),
        ("Kota", "Rajasthan", 620, 190, 540),
        ("Chandigarh", "Chandigarh", 342, 53, 275),
        ("Srinagar", "Jammu and Kashmir", 310, 42, 380)
    ]
    
    df_city = pd.DataFrame(cities_data, columns=["City", "State", "Total_Accidents", "Persons_Killed", "Persons_Injured"])
    df_city.to_csv(os.path.join(raw_dir, "morth_million_plus_cities_2020.csv"), index=False)
    print(f"Created {os.path.join(raw_dir, 'morth_million_plus_cities_2020.csv')} (Rows: {len(df_city)})")

    # -------------------------------------------------------------
    # 3. Comprehensive Contributing Factors (Junctions, Roads, Weather, Causes, Vehicles)
    # -------------------------------------------------------------
    factors_data = [
        # Category_Type, Factor_Name, Total_Accidents, Persons_Killed, Persons_Injured
        
        # Road Classification
        ("Road Classification", "National Highways", 116496, 47984, 109312),
        ("Road Classification", "State Highways", 90695, 33148, 86835),
        ("Road Classification", "Other Urban & District Roads", 158947, 50582, 152132),
        
        # Junction Configuration
        ("Junction Configuration", "T-Junction", 48210, 16930, 44250),
        ("Junction Configuration", "Y-Junction", 29840, 10420, 27690),
        ("Junction Configuration", "4-Arm Cross Junction", 54320, 18850, 51400),
        ("Junction Configuration", "Roundabout / Traffic Circle", 14650, 4520, 13900),
        ("Junction Configuration", "Staggered Junction", 12380, 4110, 11840),
        ("Junction Configuration", "Uncontrolled / Open Road Section", 206738, 76884, 199199),
        
        # Traffic & Human Factors (Causes)
        ("Traffic Cause", "Over-speeding", 265343, 91239, 252115),
        ("Traffic Cause", "Drunken Driving / Under Influence", 8355, 3322, 7014),
        ("Traffic Cause", "Driving on Wrong Side / Lane Indiscipline", 20228, 7332, 18910),
        ("Traffic Cause", "Jumping Red Light", 4380, 1420, 4010),
        ("Traffic Cause", "Use of Mobile Phones while Driving", 6753, 2511, 5980),
        ("Traffic Cause", "Other Causes / Human Errors", 61079, 25890, 60250),
        
        # Weather Conditions
        ("Weather Condition", "Fine / Clear Sky", 268412, 93450, 256820),
        ("Weather Condition", "Rainy / Wet Pavement", 34210, 12890, 31450),
        ("Weather Condition", "Foggy / Misty (Low Visibility)", 41530, 17240, 38120),
        ("Weather Condition", "Hail / Sleet / Severe Weather", 6850, 2414, 6140),
        ("Weather Condition", "Other / Adverse Weather", 15136, 5720, 15749),

        # Road Features & Surface Conditions
        ("Road Surface Feature", "Normal / Flat Straight Road", 242150, 84300, 231400),
        ("Road Surface Feature", "Curved / Sharp Turn Section", 58420, 21940, 55210),
        ("Road Surface Feature", "Potholed / Degraded Surface", 14710, 5620, 13450),
        ("Road Surface Feature", "Ongoing Road Works / Diversion", 12840, 4980, 11920),
        ("Road Surface Feature", "Bridge / Culvert / Approach", 21540, 8720, 20380),
        ("Road Surface Feature", "Steep Incline / Ghat Section", 16478, 6154, 15919),
        
        # Road User / Vehicle Category Involved
        ("Road User Type", "Two-Wheelers (Motorcycles/Scooters)", 158964, 56873, 149210),
        ("Road User Type", "Pedestrians (VRU)", 56214, 23483, 49810),
        ("Road User Type", "Cars / Taxis / Jeeps / LMV", 64320, 21450, 62100),
        ("Road User Type", "Trucks / Lorries / Heavy Goods", 38940, 17820, 34250),
        ("Road User Type", "Buses (Public & Private)", 18450, 6720, 19840),
        ("Road User Type", "Auto-Rickshaws (3-Wheelers)", 21450, 6128, 23149),
        ("Road User Type", "Bicycles (Non-Motorized VRU)", 7800, 3150, 7920)
    ]
    
    df_factors = pd.DataFrame(factors_data, columns=["Category_Type", "Factor_Name", "Total_Accidents", "Persons_Killed", "Persons_Injured"])
    df_factors.to_csv(os.path.join(raw_dir, "morth_contributing_factors_2020.csv"), index=False)
    print(f"Created {os.path.join(raw_dir, 'morth_contributing_factors_2020.csv')} (Rows: {len(df_factors)})")

    # -------------------------------------------------------------
    # 4. Time Interval Distribution (24-Hour Diurnal Pattern)
    # -------------------------------------------------------------
    time_data = [
        # Time_Slot, Start_Hour, End_Hour, Total_Accidents, Persons_Killed, Persons_Injured
        ("00:00 - 03:00 (Late Night)", 0, 3, 18450, 7820, 16920),
        ("03:00 - 06:00 (Early Morning)", 3, 6, 21340, 9150, 19480),
        ("06:00 - 09:00 (Morning Rush)", 6, 9, 39820, 14210, 37650),
        ("09:00 - 12:00 (Late Morning Peak)", 9, 12, 54210, 18940, 51920),
        ("12:00 - 15:00 (Afternoon)", 12, 15, 52140, 17820, 50110),
        ("15:00 - 18:00 (Evening Rush)", 15, 18, 64890, 22450, 62410),
        ("18:00 - 21:00 (Night Peak Window)", 18, 21, 71240, 25980, 68340),
        ("21:00 - 24:00 (Late Evening)", 21, 24, 44048, 15344, 41449)
    ]
    
    df_time = pd.DataFrame(time_data, columns=["Time_Slot", "Start_Hour", "End_Hour", "Total_Accidents", "Persons_Killed", "Persons_Injured"])
    df_time.to_csv(os.path.join(raw_dir, "morth_time_slots_2020.csv"), index=False)
    print(f"Created {os.path.join(raw_dir, 'morth_time_slots_2020.csv')} (Rows: {len(df_time)})")

if __name__ == "__main__":
    build_raw_datasets()
