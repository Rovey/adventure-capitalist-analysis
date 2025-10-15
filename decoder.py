import struct
import json
from collections import OrderedDict

def decode_adventure_communist_save(filename):
    """Decode Adventure Communist save file (FlatBuffer format)"""
    with open(filename, "rb") as f:
        data = f.read()
    
    # Check for ADCM header
    if data[4:8] != b'ADCM':
        print("❌ Not a valid Adventure Communist save file")
        return None
    
    print(f"✅ Found ADCM header")
    print(f"📊 File size: {len(data)} bytes\n")
    
    # Parse the structured data section (starts around 0x1480)
    # This contains researcher/card data as repeating 16-byte entries:
    # [4 bytes: ID][4 bytes: flags/padding][8 bytes: double value]
    
    cards = OrderedDict()
    
    # Find the start of the card data section by looking for the pattern
    # We know entries have decreasing IDs
    for start_pos in range(0x1400, 0x1500):
        try:
            # Try to find a sequence of decreasing IDs
            id1 = struct.unpack('<I', data[start_pos:start_pos+4])[0]
            id2 = struct.unpack('<I', data[start_pos+16:start_pos+20])[0]
            id3 = struct.unpack('<I', data[start_pos+32:start_pos+36])[0]
            
            if 30 < id1 < 50 and id2 == id1 - 1 and id3 == id2 - 1:
                print(f"Found card data section at 0x{start_pos:04x}")
                
                # Parse all entries
                pos = start_pos
                entry_count = 0
                while pos + 16 <= len(data) and entry_count < 100:
                    card_id = struct.unpack('<I', data[pos:pos+4])[0]
                    flags = struct.unpack('<I', data[pos+4:pos+8])[0]
                    value = struct.unpack('<d', data[pos+8:pos+16])[0]
                    
                    # Stop when card_id is clearly invalid
                    if card_id > 200:
                        break
                    
                    # Store even if value seems weird - it might be valid game data
                    cards[card_id] = {
                        'id': card_id,
                        'value': value,
                        'flags': flags
                    }
                    
                    pos += 16
                    entry_count += 1
                
                break
        except:
            continue
    
    # Parse mission progress section (quests, medals, experiments)
    mission_progress = OrderedDict()
    
    # Find mission strings and their values
    mission_keywords = [b'Capsules and Scientists', b'Medals', b'Potatoes', b'Intro', 
                       b'Medicine', b'Weapon', b'Ore', b'Land']
    
    for keyword in mission_keywords:
        pos = data.find(keyword)
        if pos != -1:
            end = data.find(b'\x00', pos)
            if end > pos:
                key = data[pos:end].decode('utf-8', errors='ignore')
                
                # Value is typically 4-8 bytes after the null terminator
                for offset in range(end + 1, min(end + 20, len(data) - 4)):
                    try:
                        val = struct.unpack('<I', data[offset:offset+4])[0]
                        if 0 <= val <= 500:  # Reasonable range
                            mission_progress[key] = val
                            break
                    except:
                        pass
    
    # Parse currency section - look for scientist currency
    # Search near the beginning for player resources
    currency = OrderedDict()
    
    # Scientists are often stored near mission data
    # Let's check the area around missions for scientist count
    scientist_pos = data.find(b'Scientists')
    if scientist_pos != -1:
        # Look in the vicinity for the actual count
        for offset in range(max(0, scientist_pos - 100), min(scientist_pos + 200, len(data) - 8)):
            try:
                val_double = struct.unpack('<d', data[offset:offset+8])[0]
                if 0 < val_double < 1000 and val_double == int(val_double):
                    # Check if this could be the scientist count
                    # by seeing if it's near other reasonable values
                    currency[f'Scientists_candidate_at_0x{offset:04x}'] = int(val_double)
            except:
                pass
    
    # Also parse the statistics section (key-value pairs with string keys)
    statistics = OrderedDict()
    offset = 0
    while offset < len(data) - 40:
        try:
            # Look for known prefixes
            if data[offset:offset+10] == b'Generator.' or \
               data[offset:offset+6] == b'Store.' or \
               data[offset:offset+5] == b'Game.' or \
               data[offset:offset+11] == b'Experiment.' or \
               data[offset:offset+6] == b'Crate.':
                
                # Read the null-terminated string
                end = data.find(b'\x00', offset)
                if end > offset and end - offset < 100:
                    key = data[offset:end].decode('utf-8', errors='ignore')
                    
                    # Look for a double value nearby (within next 40 bytes)
                    for value_offset in range(end + 1, min(end + 40, len(data) - 8)):
                        try:
                            value = struct.unpack('<d', data[value_offset:value_offset+8])[0]
                            # Check if it's a reasonable value
                            if 0 <= value < 1e15:
                                statistics[key] = value
                                break
                        except:
                            pass
        except:
            pass
        
        offset += 1
    
    return {
        'cards': cards,
        'statistics': statistics,
        'mission_progress': mission_progress,
        'currency': currency
    }

# Card/Resource names (Adventure Communist)
# Pattern observed: IDs 1-5 are total resources earned
# IDs 6-30 appear to be generator counts/costs in groups per industry
# IDs 36-38 are currencies
CARD_NAMES = {
    # === PRIMARY RESOURCES (Total Earned) ===
    1: "🥔 POTATOES (Total Earned)",
    2: "🏞️ LAND (Total Earned)",
    3: "⚔️ WEAPONS (Total Earned)",
    4: "⛏️ ORE (Total Earned)",
    5: "💊 MEDICINE (Total Earned)",
    
    # === POTATO INDUSTRY (IDs 6-10) ===
    6: "👨‍🌾 Farmer (Upgrade Cost)",
    7: "🏘️ Commune (Upgrade Cost)",
    8: "🏛️ Collective (Upgrade Cost)",
    9: "🏡 Plantation (Count/Level)",
    10: "🏢 Hive (Count/Level)",
    
    # === LAND INDUSTRY (IDs 11-15) ===
    11: "👷 Worker (Level)",
    12: "🚧 Blasting Site (Count) = 8.42e+16",
    13: "🌲 Clearcut (Upgrade Cost) = 1.35e+09",
    14: "🛣️ Road (Count) = 152",
    15: "🛤️ Highway (Count/Level)",
    
    # === ORE INDUSTRY (IDs 16-21) ===
    16: "⛏️ Super Highway (Level)",
    17: "👨‍🔧 Miner (Level)",
    18: "⛰️ Mine (Count) = 1.33e+14",
    19: "🚜 Excavator (Count) = 4.28e+06",
    20: "🏔️ Mega Mine (Level)",
    21: "🗻 Deep Bore (Count/Level)",
    
    # === WEAPONS INDUSTRY (IDs 22-27) ===
    22: "🪖 Mega Drill (Level)",
    23: "🎖️ Soldier (Level)",
    24: "👥 Fireteam (Count) = 5.29e+16",
    25: "⚔️ Squad (Upgrade Cost) = 1.28e+09",
    26: "🛡️ Platoon (Count) = 215",
    27: "🎯 Division (Count/Level)",
    
    # === MEDICINE INDUSTRY (IDs 28-33) ===
    28: "🏛️ Communist Ideal (Level)",
    29: "👨‍⚕️ Nurse (Level)",
    30: "🚑 Ambulance (Count) = 1.68e+07",
    31: "🏥 Field Hospital (Count) = 171",
    32: "🏨 Clinic (Level)",
    33: "🏩 Hospital (Count/Level)",
    
    # === OTHER ===
    34: "🧬 Cloning Lab (Count/Level)",
    35: "Card 35 (Level)",
    
    # === CURRENCIES ===
    36: "💎 SCIENTISTS (Currency)",
    37: "🥔 Potatoes (Current Resource)",
    38: "👥 COMRADES (Currency)",
    39: "Card 39",
}

# Main execution
save_file = "game.sav"
print(f"🔍 Decoding: {save_file}\n")

decoded_data = decode_adventure_communist_save(save_file)

if decoded_data:
    print("\n" + "="*70)
    print("💰 CURRENCY & RESOURCES")
    print("="*70)
    
    if decoded_data['currency']:
        for key, value in decoded_data['currency'].items():
            print(f"{key:50s}: {value}")
    else:
        print("  (No currency data found)")
    
    print("\n" + "="*70)
    print("🎯 MISSION PROGRESS & MEDALS")
    print("="*70)
    
    if decoded_data['mission_progress']:
        # Add context to known entries
        mission_labels = {
            'Intro': 'Farming Medals (Intro)',
            'Medals': 'Total Medals',
            'Potatoes': 'Potato Missions',
            'Land': 'Land Missions',
            'Ore': 'Ore Missions', 
            'Weapon': 'Weapon Missions',
            'Medicine.Earned.Total': 'Medicine/Industry Experiments',
        }
        
        for key, value in decoded_data['mission_progress'].items():
            display_key = mission_labels.get(key, key)
            print(f"{display_key:45s}: {value:5d}")
    else:
        print("  (No mission progress found)")
    
    print("\n" + "="*70)
    print("🎴 CARDS / RESEARCHERS")
    print("="*70)
    
    for card_id in sorted(decoded_data['cards'].keys(), reverse=True):
        card = decoded_data['cards'][card_id]
        name = CARD_NAMES.get(card_id, f"Card/Resource {card_id}")
        value = card['value']
        
        if value > 0:  # Only show non-zero values
            print(f"ID {card_id:3d}: {name:30s} = {value:15,.2f}")
    
    print("\n" + "="*70)
    print("📈 STATISTICS")
    print("="*70)
    
    for key, value in decoded_data['statistics'].items():
        if value > 0:  # Only show non-zero values
            print(f"{key:50s}: {value:15,.2f}")
    
    # Save to JSON
    output = {
        'currency': decoded_data['currency'],
        'mission_progress': decoded_data['mission_progress'],
        'cards': {k: v['value'] for k, v in decoded_data['cards'].items()},
        'statistics': decoded_data['statistics']
    }
    
    with open("decoded_save.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "="*70)
    print("✅ Full data saved to: decoded_save.json")
    print("="*70)
else:
    print("❌ Failed to decode save file")
