CLASSES = [
            # Пехота
            """military soldier with weapon, combat gear, uniform, may wear helmet or not, can carry rifle or other weapons,
            can be unarmed, standing walking or running, on ground, sometimes on top of vehicles""",
                
            # Танк
            """main battle tank, heavy armored vehicle with large caliber cannon in rotating turret, thick armor,
            tracks, soldiers can sit on top but not carried inside, military""",
                
            # БМП
            """infantry fighting vehicle, medium armored vehicle with autocannon, smaller cannon than tank, thinner armor than tank,
            carries troops inside, smaller turret than tank, faster than tank, has firing ports, tracks, military""",
                
            # БТР
            """armored personnel carrier, wheeled transport vehicle, machine gun armed, carries troops, any wheel configuration,
            smaller caliber than BMP, faster than BMP, military""",
                
            # Бронемашина
            """light armored vehicle, military truck with armor, reconnaissance, fast, wheels,
            may have machine gun on roof but no turret, scouting, not for combat""",
                
            # Артиллерия
            """artillery, howitzer, field gun, self-propelled artillery with single long barrel, very large caliber cannon,
            huge gun, lightly armored or unarmored, tracks or wheels, military""",
                
            # РСЗО
            """multiple rocket launcher system, flat roof, no turret, only rocket tubes, never have a gun barrel, 
            front like a truck, never has tracks, always have many rockets on back, """,
                
            # Дрон
            """drone, military UAV, unmanned aerial vehicle, quadcopter or fixed-wing drone, flying object,
            small military aircraft, can move in all directions unlike planes, has propellers and thin legs"""
]


CLASSES_MAP = {
            CLASSES[0]: 'Пехота',
            CLASSES[1]: 'Танк',
            CLASSES[2]: 'БМП (Боевая Машина Пехоты)',
            CLASSES[3]: 'БТР (Бронетранспортер)',
            CLASSES[4]: 'Бронемашина',
            CLASSES[5]: 'Артиллерия',
            CLASSES[6]: 'РСЗО (Ракетная Система Залпового Огня)',
            CLASSES[7]: 'БПЛА (Беспилотный Летательный Аппарат)',
        }

FINETUNED_MAP = [
            'Пехота',
            'Танк',
            'БМП (Боевая Машина Пехоты)',
            'БТР (Бронетранспортер)',
            'Бронемашина',
            'Артиллерия',
            'РСЗО (Ракетная Система Залпового Огня)',
            'БПЛА (Беспилотный Летательный Аппарат)',
]

confidence_threshold = 0.4
