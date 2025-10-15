"""
Command-line Experiments ROI analysis tool for Adventure Communist
Shows which experiments give the best return on investment
"""

import sys
from decoder_gui import decode_adventure_communist_save
from experiments_roi import analyze_experiments, format_experiment_recommendations, get_industry_production_ranking


def main():
    # Get save file path
    if len(sys.argv) > 1:
        save_path = sys.argv[1]
    else:
        save_path = "game.sav"
    
    print(f"Analyzing experiments from: {save_path}\n")
    
    # Decode save file
    decoded_data = decode_adventure_communist_save(save_path)
    
    if not decoded_data:
        print("Error: Could not decode save file")
        return 1
    
    # Show industry production ranking
    print("\n" + "="*90)
    print("INDUSTRY PRODUCTION RANKING (Focus on weakest industries)")
    print("="*90)
    production = get_industry_production_ranking(decoded_data)
    for i, (industry, value) in enumerate(production.items(), 1):
        bar = "#" * min(50, int(value / max(production.values()) * 50)) if value > 0 else ""
        print(f"{i}. {industry:10} {value:12.2e} {bar}")
    
    # Analyze experiments
    recommendations, current_scientists = analyze_experiments(decoded_data)
    
    # Display results
    output = format_experiment_recommendations(recommendations, current_scientists, top_n=20)
    print("\n" + output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
