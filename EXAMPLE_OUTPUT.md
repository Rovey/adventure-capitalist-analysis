# Example Decoder Output

This is what the decoder output looks like when processing a save file:

```
Decoding: game.sav

✅ Found ADCM header
📊 File size: 7216 bytes

Found card data section at 0x14a8
================================================================================
CURRENCIES
================================================================================
Scientists: 43
Comrades:   5.53e+10

================================================================================
MISSION PROGRESS & MEDALS
================================================================================
Capsules and Scientists,Begin,3:     4
Total Medals                  :    23
Potato Missions               :     5
Farming Medals                :     6
Industry Experiments          :    12
Weapon.Earned.Total           :     8
Ore.Earned.Total              :    16
Land.Earned.Total             :    16

================================================================================
TOTAL RESOURCES EARNED
================================================================================
POTATOES (Total Earned)       : 5.64e+35
LAND (Total Earned)           : 1.24e+26
WEAPONS (Total Earned)        : 2.85e+22
ORE (Total Earned)            : 1.51e+25
MEDICINE (Total Earned)       : 3.52e+20

================================================================================
GENERATORS & UPGRADES
================================================================================

POTATO:
  [ 6] Farmer (Upgrade Cost)         : 2.06e+23
  [ 7] Commune (Upgrade Cost)        : 1.05e+15
  [ 8] Collective (Upgrade Cost)     : 3.56e+07
  [ 9] Plantation (Count/Level)      : 6

LAND:
  [11] Worker (Level)                : 1
  [12] Blasting Site (Count)         : 8.42e+16
  [13] Clearcut (Upgrade Cost)       : 1.35e+09
  [14] Road (Count)                  : 152

ORE:
  [17] Miner (Level)                 : 1
  [18] Mine (Count)                  : 1.33e+14
  [19] Excavator (Count)             : 4.28e+06
  [20] Mega Mine (Level)             : 1

WEAPONS:
  [23] Soldier (Level)               : 1
  [24] Fireteam (Count)              : 5.29e+16
  [25] Squad (Upgrade Cost)          : 1.28e+09
  [26] Platoon (Count)               : 215

MEDICINE:
  [29] Nurse (Level)                 : 1
  [30] Ambulance (Count)             : 1.68e+07
  [31] Field Hospital (Count)        : 171
  [32] Clinic (Level)                : 1

================================================================================
Data saved to: decoded_save.json
================================================================================
```

## JSON Output

The `decoded_save.json` file contains:

```json
{
  "currency": {
    "scientists": 43,
    "comrades": 55277928194
  },
  "mission_progress": {
    "Capsules and Scientists,Begin,3": 4,
    "Medals": 23,
    "Potatoes": 5,
    "Intro": 6,
    "Medicine.Earned.Total": 12,
    "Weapon.Earned.Total": 8,
    "Ore.Earned.Total": 16,
    "Land.Earned.Total": 16
  },
  "cards": {
    "1": 5.642828422260094e+35,
    "2": 1.2415097626654276e+26,
    "3": 2.849113776431087e+22,
    "4": 1.5057081191241972e+25,
    "5": 3.5202688269758967e+20,
    "6": 2.0631898886519682e+23,
    "7": 1054594450897455.0,
    "8": 35577316.0,
    ...
  }
}
```
