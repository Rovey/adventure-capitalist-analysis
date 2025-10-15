# Adventure Communist Save File Decoder & Experiments Analyzer

A Python tool to decode and analyze Adventure Communist save files, with intelligent recommendations for which experiments to research next.

## Features

- **Save File Decoding**: Parses Adventure Communist binary save files (FlatBuffer format with ADCM header)
- **Game State Extraction**:
  - Scientists and Comrades currencies
  - Total resources earned per industry
  - Generator counts and levels
  - Mission progress and medals
  - Industry experiments completed
- **Experiments ROI Analysis**: Smart recommendations for which experiments to research
  - Ranks all affordable experiments by impact per Scientist spent
  - Prioritizes permanent INDUSTRY multipliers (x99999, x9999, x999)
  - Automatically prioritizes weakest industries when ROI scores are equal
  - Shows industry production ranking to identify bottlenecks
  - Distinguishes between permanent upgrades and temporary boosts
- **GUI Application**: Easy-to-use graphical interface
  - Auto-detects Steam save file location
  - Real-time decoding and analysis
  - Export data to JSON

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Rovey/adventure-capitalist-analysis.git
cd adventure-capitalist-analysis
```

2. Ensure Python 3.6+ is installed

**No additional dependencies required** - uses only Python standard library!

## Quick Start

### GUI Application (Recommended)

```bash
python decoder_gui.py
```

**How to use:**
1. GUI auto-detects your Steam save location
2. Click **"Decode Save"** to view your game data
3. Click **"Analyze Experiments"** to see recommendations
4. Go to EXPERIMENTS tab in-game and buy the top recommendation!

### Command Line Analysis

```bash
python analyze_experiments.py game.sav
```

Or specify a custom save file path:
```bash
python analyze_experiments.py "C:\Path\To\game.sav"
```

## Finding Your Save File

### Windows (Steam)
```
C:\Program Files (x86)\Steam\userdata\[USER_ID]\462930\remote\game.sav
```

Where `[USER_ID]` is your Steam user ID (a folder with numbers). If you have multiple user folders, look for the one with the most recent `game.sav`.

The GUI automatically detects this location!

### Verify Save File

Valid Adventure Communist save files:
- Have `.sav` extension
- Are 5-15 KB in size
- Contain "ADCM" magic header at byte offset 0x04

## Understanding the Experiments Analysis

### Experiment Types

**INDUSTRY Experiments** (PERMANENT - Highest Priority!)
- `Best-est` buttons: x99,999 multiplier (60 Scientists)
- `Better-est` buttons: x9,999 multiplier (45 Scientists)
- `Better-er` buttons: x999 multiplier (30 Scientists)
- These are **permanent** and provide the best long-term value

**STATE Experiments** (Utility)
- `Button Auto-Clickers`: Automatically clicks production buttons (25 Scientists)
- `Big Resource Surge`: 4 hours of resources instantly (50 Scientists)
- `Mega Resource Surge`: 24 hours of resources instantly (150 Scientists)

**TRIALS Experiments** (Temporary)
- `Button Blasts`: x7,777 multiplier for 20-30 seconds (5-10 Scientists)
- Only useful for completing specific missions

### ROI Score Explained

**ROI Score = (Production Increase × Priority) / Cost**

- Higher score = Better value per Scientist
- Example: x99,999 for 60 Scientists = ROI of 16,666
- Example: x999 for 30 Scientists = ROI of 233

### Smart Tiebreaking

When experiments have equal ROI scores, the analyzer automatically prioritizes your **weakest industries**:

**Priority order:** Medicine → Weapons → Ore → Land → Potato

This ensures balanced progress across all industries!

### Sample Output

```
INDUSTRY PRODUCTION RANKING (Focus on weakest)
==================================================================================
1. Medicine       3.06e+20  ← WEAKEST! 
2. Ore            1.27e+22
3. Weapons        1.06e+25
4. Land           7.84e+25
5. Potato         5.73e+35  ← STRONGEST!

Current Scientists: 105

TOP 5 AFFORDABLE EXPERIMENTS:

1. Best-est Medicine Button
   INDUSTRY | Medicine | Cost: 60 | Effect: x99,999
   ROI: 16666.50 | Priority: 10/10
   → MEDICINE production x99999 - HUGE permanent boost

2. Best-est Weapon Button
   INDUSTRY | Weapons | Cost: 60 | Effect: x99,999
   ROI: 16666.50 | Priority: 10/10
   → WEAPONS production x99999 - HUGE permanent boost
```

## Strategy Guide

### Best Practices

1. **Always prioritize INDUSTRY experiments** - They're permanent and give huge boosts
2. **Focus on your weakest industry** - The tool automatically shows you which needs help
3. **Get Button Auto-Clickers early** - Quality of life improvement worth the cost
4. **Avoid temporary boosts** - Only buy TRIALS experiments when needed for missions
5. **Save for big multipliers** - x99,999 boosts are worth waiting for

### Example Decision Making

**You have 105 Scientists:**

**Option 1: Maximum Impact**
- Buy `Best-est Medicine Button` (60 Scientists) - x99,999 permanent boost
- Remaining: 45 Scientists for next upgrade

**Option 2: Multiple Upgrades**
- Buy `Better-est Medicine Button` (45 Scientists) - x9,999 boost
- Buy `Button Auto-Clickers` (25 Scientists) - Automation
- Remaining: 35 Scientists

**Option 3: Save Up**
- Don't buy anything yet
- Wait until 120 Scientists
- Buy two x99,999 boosts back-to-back

### When to Buy What

| Scientists | Best Purchase | Why |
|-----------|--------------|-----|
| 5-25 | Save up | Too small for meaningful impact |
| 25-29 | Button Auto-Clickers | Quality of life |
| 30-44 | x999 Multiplier (weakest industry) | Good permanent boost |
| 45-59 | x9,999 Multiplier (weakest industry) | Strong permanent boost |
| 60+ | x99,999 Multiplier (weakest industry) | HUGE permanent boost |

## Technical Details

### Save File Format

- **Format**: FlatBuffer binary format
- **Magic Header**: "ADCM" at offset 0x04
- **Card Data**: 16-byte entries (4 bytes ID + 4 bytes flags + 8 bytes double value)
- **Card Data Location**: Typically around offset 0x14a8-0x1540 (varies by save file size)

### Card ID Mapping

| Card ID | Data |
|---------|------|
| 1-5 | Total resources earned (Potatoes, Land, Ore, Weapons, Medicine) |
| 6-33 | Generator counts by industry |
| 36 | Scientists currency |
| 38 | Comrades currency |

### Experiments Database

The `experiments_roi.py` module contains a complete database of all 30+ experiments in Adventure Communist with accurate costs and effects.

## Output Files

- **decoded_save.json**: Exported game data (created in same directory as save file)
- Contains: currencies, mission progress, all card values
- Useful for tracking progress over time or custom analysis

## Privacy Note

⚠️ **Never share your save files publicly!** They contain:
- Your game progress
- Potential account identifiers
- Purchase history

The `.gitignore` file is configured to exclude:
- `*.sav` files
- `decoded_save.json`
- Personal game data

## Troubleshooting

### "No ADCM header found"
- Ensure you're loading a valid `.sav` file
- Verify it's Adventure **Communist** (not Adventure Capitalist)
- Check file isn't corrupted

### "Found 0 cards" or "Scientists: 0"
- This was a bug in older versions - now fixed!
- The tool now searches a wider offset range (0x1400-0x1600)
- Update to latest version if you see this

### Steam path not auto-detected
- GUI looks in default Steam installation
- Use Browse button to manually select save file
- Verify Steam is installed at `C:\Program Files (x86)\Steam`

### GUI doesn't open
- Ensure Python has tkinter: `python -m tkinter`
- Try command-line tool instead: `analyze_experiments.py`
- Check Python version is 3.6+

## Project Structure

```
adventure-capitalist-analysis/
├── decoder.py              # Core decoding functions
├── decoder_gui.py          # GUI application
├── experiments_roi.py      # Experiments database and ROI logic
├── analyze_experiments.py  # Command-line analysis tool
├── README.md              # This file
├── LICENSE                # MIT License
└── .gitignore            # Excludes personal save files
```

## Development

### Running Tests

The decoder can be imported and used programmatically:

```python
from decoder import decode_adventure_communist_save
from experiments_roi import analyze_experiments

# Decode save file
decoded_data = decode_adventure_communist_save("game.sav")

# Analyze experiments
recommendations, scientists = analyze_experiments(decoded_data)

# Process recommendations
for rec in recommendations[:5]:
    print(f"{rec['name']}: {rec['cost']} Scientists")
```

### Contributing

Contributions welcome! Areas for improvement:
- Additional experiment data (if new updates add more)
- Better level estimation algorithms
- Support for other save file locations (Android, iOS)
- Historical progress tracking

## Credits

- **Game**: Adventure Communist by Hyper Hippo
- **Analysis**: Understanding game mechanics through save file reverse engineering
- **Format**: FlatBuffers binary format

## License

MIT License - See LICENSE file for details.

## Disclaimer

This tool is for educational purposes and personal use. It does not modify game files or provide any unfair advantages - it simply helps you make informed decisions about which experiments to research based on your current game state.

---

**Made with ❤️ for Adventure Communist players who want to optimize their progress!**

Last Updated: October 15, 2025
