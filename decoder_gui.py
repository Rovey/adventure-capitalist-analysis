"""
GUI and decoder for Adventure Communist save files.
Decodes binary FlatBuffer format and analyzes experiments ROI.
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
import struct
import json
from collections import OrderedDict
from experiments_roi import (
    analyze_experiments,
    format_experiment_recommendations,
    get_industry_production_ranking,
)


def decode_adventure_communist_save(filename):
    """Decode Adventure Communist save file (FlatBuffer format)."""
    with open(filename, "rb") as f:
        data = f.read()

    # Check for ADCM header
    if data[4:8] != b"ADCM":
        return None

    cards = OrderedDict()

    # Find the card data section (search wider range as offset can vary)
    for start_pos in range(0x1400, 0x1600):
        try:
            id1 = struct.unpack("<I", data[start_pos : start_pos + 4])[0]
            id2 = struct.unpack("<I", data[start_pos + 16 : start_pos + 20])[0]
            id3 = struct.unpack("<I", data[start_pos + 32 : start_pos + 36])[0]

            if 30 < id1 < 50 and id2 == id1 - 1 and id3 == id2 - 1:
                pos = start_pos
                entry_count = 0
                while pos + 16 <= len(data) and entry_count < 100:
                    card_id = struct.unpack("<I", data[pos : pos + 4])[0]
                    flags = struct.unpack("<I", data[pos + 4 : pos + 8])[0]
                    value = struct.unpack("<d", data[pos + 8 : pos + 16])[0]

                    if card_id > 200:
                        break

                    cards[card_id] = {"id": card_id, "value": value, "flags": flags}

                    pos += 16
                    entry_count += 1
                break
        except:
            continue

    # Parse mission progress
    mission_progress = OrderedDict()
    mission_keywords = [
        b"Capsules and Scientists",
        b"Medals",
        b"Potatoes",
        b"Intro",
        b"Medicine",
        b"Weapon",
        b"Ore",
        b"Land",
    ]

    for keyword in mission_keywords:
        pos = data.find(keyword)
        if pos != -1:
            end = data.find(b"\x00", pos)
            if end > pos:
                key = data[pos:end].decode("utf-8", errors="ignore")
                for offset in range(end + 1, min(end + 20, len(data) - 4)):
                    try:
                        val = struct.unpack("<I", data[offset : offset + 4])[0]
                        if 0 <= val <= 500:
                            mission_progress[key] = val
                            break
                    except:
                        pass

    # Note: Researched experiments are stored as IDs in the binary format
    # The save file doesn't contain easily extractable experiment data
    # Users need to manually track which experiments they've researched

    return {
        "cards": cards,
        "mission_progress": mission_progress,
    }


# Card names mapping
CARD_NAMES = {
    1: "POTATOES (Total Earned)",
    2: "LAND (Total Earned)",
    3: "WEAPONS (Total Earned)",
    4: "ORE (Total Earned)",
    5: "MEDICINE (Total Earned)",
    6: "Farmer (Upgrade Cost)",
    7: "Commune (Upgrade Cost)",
    8: "Collective (Upgrade Cost)",
    9: "Plantation (Count/Level)",
    10: "Hive (Count/Level)",
    11: "Worker (Level)",
    12: "Blasting Site (Count)",
    13: "Clearcut (Upgrade Cost)",
    14: "Road (Count)",
    15: "Highway (Count/Level)",
    16: "Super Highway (Level)",
    17: "Miner (Level)",
    18: "Mine (Count)",
    19: "Excavator (Count)",
    20: "Mega Mine (Level)",
    21: "Deep Bore (Count/Level)",
    22: "Mega Drill (Level)",
    23: "Soldier (Level)",
    24: "Fireteam (Count)",
    25: "Squad (Upgrade Cost)",
    26: "Platoon (Count)",
    27: "Division (Count/Level)",
    28: "Communist Ideal (Level)",
    29: "Nurse (Level)",
    30: "Ambulance (Count)",
    31: "Field Hospital (Count)",
    32: "Clinic (Level)",
    33: "Hospital (Count/Level)",
    34: "Cloning Lab (Count/Level)",
    35: "Card 35 (Level)",
    36: "SCIENTISTS",
    37: "Potatoes (Current Resource)",
    38: "COMRADES",
    39: "Card 39",
}


class AdventureDecoderGUI:
    """Main GUI application for decoding Adventure Communist save files."""

    def __init__(self, root):
        self.root = root
        self.root.title("Adventure Communist Save Decoder")
        self.root.geometry("900x700")

        # Initialize data storage
        self.decoded_data = None

        # Detect Steam save path
        self.default_path = self.detect_steam_path()

        # Create GUI elements
        self.create_widgets()

        # Try to load save file automatically if found
        if self.default_path and os.path.exists(self.default_path):
            self.path_var.set(self.default_path)
            self.load_button.config(state="normal")

    def detect_steam_path(self):
        """Detect Steam save file location"""
        steam_base = r"C:\Program Files (x86)\Steam\userdata"

        if not os.path.exists(steam_base):
            return None

        try:
            # Find first directory in userdata
            user_dirs = [
                d
                for d in os.listdir(steam_base)
                if os.path.isdir(os.path.join(steam_base, d))
            ]

            if user_dirs:
                user_id = user_dirs[0]
                save_path = os.path.join(
                    steam_base, user_id, "462930", "remote", "game.sav"
                )

                # Check if the directory structure exists
                remote_dir = os.path.join(steam_base, user_id, "462930", "remote")
                if os.path.exists(remote_dir):
                    # Check if game.sav exists
                    if os.path.exists(save_path):
                        return save_path
                    # Return directory if save doesn't exist yet
                    return remote_dir
        except Exception as e:
            print(f"Error detecting Steam path: {e}")

        return None

    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Top frame for file selection
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N))

        # Path label and entry
        ttk.Label(top_frame, text="Save File Path:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )

        self.path_var = tk.StringVar(value=self.default_path or "")
        path_entry = ttk.Entry(top_frame, textvariable=self.path_var, width=60)
        path_entry.grid(row=0, column=1, padx=5, pady=5)

        # Browse button
        browse_btn = ttk.Button(top_frame, text="Browse...", command=self.browse_file)
        browse_btn.grid(row=0, column=2, padx=5, pady=5)

        # Load button
        self.load_button = ttk.Button(
            top_frame, text="Decode Save", command=self.load_save, state="normal"
        )
        self.load_button.grid(row=0, column=3, padx=5, pady=5)

        # Experiments ROI Analysis button
        self.roi_button = ttk.Button(
            top_frame,
            text="Analyze Experiments",
            command=self.analyze_roi,
            state="disabled",
        )
        self.roi_button.grid(row=0, column=4, padx=5, pady=5)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            top_frame, textvariable=self.status_var, foreground="blue"
        )
        status_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=5)

        # Output text area with scrollbar
        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.output_text = scrolledtext.ScrolledText(
            output_frame, width=100, height=35, font=("Consolas", 9)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

    def browse_file(self):
        """Open file browser to select save file"""
        initial_dir = (
            os.path.dirname(self.path_var.get()) if self.path_var.get() else None
        )

        filename = filedialog.askopenfilename(
            title="Select Adventure Communist Save File",
            initialdir=initial_dir,
            filetypes=[("Save files", "*.sav"), ("All files", "*.*")],
        )

        if filename:
            # Validate that it's a .sav file
            if not filename.endswith(".sav"):
                self.status_var.set("Error: Please select a .sav file")
                return

            self.path_var.set(filename)
            self.load_button.config(state="normal")
            self.status_var.set("File selected")

    def load_save(self):
        """Load and decode the save file"""
        filepath = self.path_var.get()

        if not filepath:
            self.status_var.set("Error: No file selected")
            return

        # Handle directory path - look for game.sav
        if os.path.isdir(filepath):
            game_sav = os.path.join(filepath, "game.sav")
            if os.path.exists(game_sav):
                filepath = game_sav
                self.path_var.set(filepath)
            else:
                self.status_var.set("Error: game.sav not found in directory")
                return

        if not os.path.exists(filepath):
            self.status_var.set("Error: File not found")
            return

        if not filepath.endswith(".sav"):
            self.status_var.set("Error: File must end with .sav")
            return

        try:
            self.status_var.set("Decoding...")
            self.root.update()

            # Decode the save file
            decoded_data = decode_adventure_communist_save(filepath)

            if not decoded_data:
                self.status_var.set("Error: Invalid save file (no ADCM header)")
                return

            # Display results
            self.display_results(decoded_data, filepath)
            self.status_var.set(f"Successfully decoded: {os.path.basename(filepath)}")

        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error decoding save file:\n{str(e)}")

    def display_results(self, decoded_data, filepath):
        """Display decoded data in the text area"""
        # Store decoded data for ROI analysis
        self.decoded_data = decoded_data
        self.roi_button.config(state="normal")

        self.output_text.delete(1.0, tk.END)

        output = []
        output.append(f"Decoded: {filepath}\n")
        output.append("=" * 80)
        output.append("\nCURRENCIES")
        output.append("=" * 80)

        scientists = decoded_data["cards"].get(36, {}).get("value", 0)
        comrades = decoded_data["cards"].get(38, {}).get("value", 0)
        output.append(f"Scientists: {scientists:,.0f}")
        output.append(f"Comrades:   {comrades:,.2e}\n")

        # Mission progress
        output.append("=" * 80)
        output.append("MISSION PROGRESS & MEDALS")
        output.append("=" * 80)

        if decoded_data["mission_progress"]:
            mission_labels = {
                "Intro": "Farming Medals",
                "Medals": "Total Medals",
                "Potatoes": "Potato Missions",
                "Land": "Land Missions",
                "Ore": "Ore Missions",
                "Weapon": "Weapon Missions",
                "Medicine.Earned.Total": "Industry Experiments",
            }

            for key, value in decoded_data["mission_progress"].items():
                display_key = mission_labels.get(key, key)
                output.append(f"{display_key:30s}: {value:5d}")


        # Resources
        output.append("\n" + "=" * 80)
        output.append("TOTAL RESOURCES EARNED")
        output.append("=" * 80)

        resource_ids = [1, 2, 3, 4, 5]
        for card_id in resource_ids:
            if card_id in decoded_data["cards"]:
                card = decoded_data["cards"][card_id]
                name = CARD_NAMES.get(card_id, f"Resource {card_id}")
                value = card["value"]
                output.append(f"{name:30s}: {value:.2e}")

        # Generators by industry
        output.append("\n" + "=" * 80)
        output.append("GENERATORS & UPGRADES")
        output.append("=" * 80)

        industries = {
            "POTATO": range(6, 11),
            "LAND": range(11, 16),
            "ORE": range(16, 22),
            "WEAPONS": range(22, 28),
            "MEDICINE": range(28, 34),
        }

        for industry_name, id_range in industries.items():
            has_data = False
            industry_lines = []

            for card_id in id_range:
                if card_id in decoded_data["cards"]:
                    card = decoded_data["cards"][card_id]
                    value = card["value"]
                    if value > 0:
                        has_data = True
                        name = CARD_NAMES.get(card_id, f"Card {card_id}")
                        if value > 1e6:
                            industry_lines.append(
                                f"  [{card_id:2d}] {name:30s}: {value:.2e}"
                            )
                        else:
                            industry_lines.append(
                                f"  [{card_id:2d}] {name:30s}: {value:,.0f}"
                            )

            if has_data:
                output.append(f"\n{industry_name}:")
                output.extend(industry_lines)

        # Display in text widget
        self.output_text.insert(tk.END, "\n".join(output))

        # Save to JSON
        try:
            json_path = os.path.join(os.path.dirname(filepath), "decoded_save.json")
            output_data = {
                "currency": {"scientists": scientists, "comrades": comrades},
                "mission_progress": decoded_data["mission_progress"],
                "cards": {k: v["value"] for k, v in decoded_data["cards"].items()},
            }

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2)

            self.output_text.insert(tk.END, f"\n\n{'=' * 80}\n")
            self.output_text.insert(tk.END, f"Data saved to: {json_path}\n")
            self.output_text.insert(tk.END, "=" * 80)
        except Exception as e:
            print(f"Error saving JSON: {e}")

    def analyze_roi(self):
        """Analyze and display Experiments ROI recommendations"""
        if not hasattr(self, "decoded_data") or not self.decoded_data:
            self.status_var.set("Error: No save file loaded")
            return

        try:
            self.status_var.set("Analyzing Experiments...")
            self.root.update()

            # Show industry ranking
            self.output_text.delete(1.0, tk.END)

            output = []
            output.append("=" * 90)
            output.append("INDUSTRY PRODUCTION RANKING (Focus on weakest)")
            output.append("=" * 90 + "\n")

            production = get_industry_production_ranking(self.decoded_data)
            for i, (industry, value) in enumerate(production.items(), 1):
                progress_bar = (
                    "█" * min(40, int(value / max(production.values()) * 40))
                    if value > 0
                    else ""
                )
                output.append(f"{i}. {industry:10} {value:12.2e} {progress_bar}")

            self.output_text.insert(tk.END, "\n".join(output) + "\n\n")

            # Analyze experiments
            # Note: Save file doesn't store which specific experiments are researched
            # User needs to manually update KNOWN_RESEARCHED in experiments_roi.py
            recommendations, current_scientists = analyze_experiments(self.decoded_data)

            # Display results
            exp_output = format_experiment_recommendations(
                recommendations, current_scientists, top_n=20
            )
            self.output_text.insert(tk.END, exp_output)

            status_msg = (
                f"Experiments Analysis Complete - "
                f"{len(recommendations)} experiments analyzed"
            )
            self.status_var.set(status_msg)

        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(
                tk.END, f"Error analyzing experiments:\n{str(e)}\n\n"
            )
            import traceback

            self.output_text.insert(tk.END, traceback.format_exc())


def main():
    root = tk.Tk()
    app = AdventureDecoderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
