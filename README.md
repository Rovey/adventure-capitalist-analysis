# Adventure Communist Save File Decoder

A Python tool to decode and analyze Adventure Communist game save files. This decoder extracts game state information including currencies, resources, generators, and mission progress from the binary FlatBuffer save format.

## Features

- **Decode Binary Save Files**: Reads `.sav` files with the ADCM (Adventure Communist) format
- **Extract Game Data**:
  - Scientists and Comrades currencies
  - Total resources earned across all industries
  - Generator counts and upgrade costs
  - Mission progress and medals
- **Clean Output**: Organized display of game state by industry
- **JSON Export**: Saves decoded data to JSON for further analysis

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd adventure-capitalist-analysis
```

2. Ensure Python 3.6+ is installed

No additional dependencies required - uses only Python standard library!

## Usage

### GUI Application (Recommended)

Run the graphical interface:

```bash
python decoder_gui.py
```

The GUI will:
- **Auto-detect Steam save location**: Automatically finds your Adventure Communist save in `C:\Program Files (x86)\Steam\userdata\[USER_ID]\462930\remote\game.sav`
- **Browse for files**: Select any `.sav` file from any location
- **Real-time decoding**: View results instantly in the application
- **Export to JSON**: Automatically saves decoded data

### Command Line Usage

Place your Adventure Communist save file in the project directory and rename it to `game.sav`, then run:

```bash
python decoder.py
```

### Finding Your Save File

Adventure Communist save files are typically located at:
- **Windows**: `%LOCALAPPDATA%\Packages\[AdventureCommPackage]\LocalState\`
- **Android**: Use a file manager with root access to find the save in the game's data directory

The save files have a `.sav` extension and contain "ADCM" as a magic header.

## Output

The decoder displays:

### 1. Currencies
```
Scientists: 43
Comrades:   5.53e+10
```

### 2. Mission Progress
```
Farming Medals: 6
Total Medals: 23
Industry Experiments: 12
```

### 3. Total Resources Earned
```
POTATOES (Total Earned): 5.64e+35
LAND (Total Earned): 1.24e+26
ORE (Total Earned): 1.51e+25
WEAPONS (Total Earned): 2.85e+22
MEDICINE (Total Earned): 3.52e+20
```

### 4. Generators by Industry
Organized by POTATO, LAND, ORE, WEAPONS, and MEDICINE industries, showing:
- Generator counts
- Upgrade costs
- Current levels

## Data Structure

The decoder identifies the following card/resource IDs:

| ID Range | Description |
|----------|-------------|
| 1-5 | Total resources earned per industry |
| 6-10 | Potato industry generators |
| 11-15 | Land industry generators |
| 16-21 | Ore industry generators |
| 22-27 | Weapons industry generators |
| 28-33 | Medicine industry generators |
| 36 | Scientists currency |
| 37 | Current potato resource amount |
| 38 | Comrades currency |

## Output Files

- `decoded_save.json`: Complete decoded data in JSON format for further analysis

## Technical Details

### Save File Format

Adventure Communist uses a FlatBuffer binary format with:
- Magic header: `ADCM` at offset 0x04
- Card data section: 16-byte entries at ~0x14a8
  - 4 bytes: Card ID (uint32)
  - 4 bytes: Flags (uint32)
  - 8 bytes: Value (double)

### Card Data Structure

Each card entry contains:
- **ID**: Unique identifier for the resource/generator
- **Flags**: Additional metadata (currently unused)
- **Value**: Count, cost, or amount (stored as double-precision float)

## Use Cases

- **Progress Tracking**: Monitor your game progression over time
- **ROI Analysis**: Calculate return on investment for researcher upgrades
- **Save Comparison**: Compare different save states to optimize strategy
- **Data Export**: Extract data for spreadsheet analysis

## Contributing

Contributions welcome! Areas for improvement:
- Identifying remaining unknown card IDs
- Decoding researcher card data
- Parsing additional game statistics
- Adding visualization tools

## License

See LICENSE file for details.

## Disclaimer

This tool is for educational and personal use only. It reads game save files but does not modify them. Use at your own risk.

## Acknowledgments

- Reverse engineering of the FlatBuffer save format
- Adventure Communist game by Hyper Hippo Productions
