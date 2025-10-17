"""
Experiments ROI Calculator for Adventure Communist
Analyzes which experiment upgrades give the best return on investment
Based on actual game mechanics from the EXPERIMENTS section
"""

# EXPERIMENTS data based on Adventure Communist game mechanics
# Format: {name: {'cost': scientists, 'type': category, 'multiplier': boost, 'priority': importance}}

EXPERIMENTS = {
    # INDUSTRY Tab - Permanent multipliers (HIGHEST PRIORITY)
    "Button Auto-Clickers": {
        "cost": 25,
        "type": "STATE",
        "multiplier": "Auto-click all buttons",
        "boost": "Passive",
        "priority": 9,
        "description": "Automatically clicks production buttons - massive time saver",
    },
    # x99999 Multipliers - Industry-wide permanent boosts
    "Best-est Potato Button": {
        "cost": 60,
        "type": "INDUSTRY",
        "multiplier": 99999,
        "boost": "Potato",
        "priority": 10,
        "description": "POTATO production x99999 - HUGE permanent boost",
    },
    "Best-est Land Button": {
        "cost": 60,
        "type": "INDUSTRY",
        "multiplier": 99999,
        "boost": "Land",
        "priority": 10,
        "description": "LAND production x99999 - HUGE permanent boost",
    },
    "Best-est Weapon Button": {
        "cost": 60,
        "type": "INDUSTRY",
        "multiplier": 99999,
        "boost": "Weapons",
        "priority": 10,
        "description": "WEAPONS production x99999 - HUGE permanent boost",
    },
    "Best-est Ore Button": {
        "cost": 60,
        "type": "INDUSTRY",
        "multiplier": 99999,
        "boost": "Ore",
        "priority": 10,
        "description": "ORE production x99999 - HUGE permanent boost",
    },
    "Best-est Medicine Button": {
        "cost": 60,
        "type": "INDUSTRY",
        "multiplier": 99999,
        "boost": "Medicine",
        "priority": 10,
        "description": "MEDICINE production x99999 - HUGE permanent boost",
    },
    # x9999 Multipliers - Slightly lower tier
    "Better-est Potato Button": {
        "cost": 45,
        "type": "INDUSTRY",
        "multiplier": 9999,
        "boost": "Potato",
        "priority": 8,
        "description": "POTATO production x9999 - Very strong boost",
    },
    "Better-est Land Button": {
        "cost": 45,
        "type": "INDUSTRY",
        "multiplier": 9999,
        "boost": "Land",
        "priority": 8,
        "description": "LAND production x9999 - Very strong boost",
    },
    "Better-est Weapon Button": {
        "cost": 45,
        "type": "INDUSTRY",
        "multiplier": 9999,
        "boost": "Weapons",
        "priority": 8,
        "description": "WEAPONS production x9999 - Very strong boost",
    },
    "Better-est Ore Button": {
        "cost": 45,
        "type": "INDUSTRY",
        "multiplier": 9999,
        "boost": "Ore",
        "priority": 8,
        "description": "ORE production x9999 - Very strong boost",
    },
    "Better-est Medicine Button": {
        "cost": 45,
        "type": "INDUSTRY",
        "multiplier": 9999,
        "boost": "Medicine",
        "priority": 8,
        "description": "MEDICINE production x9999 - Very strong boost",
    },
    # x999 Multipliers
    "Better-er Potato Button": {
        "cost": 30,
        "type": "INDUSTRY",
        "multiplier": 999,
        "boost": "Potato",
        "priority": 7,
        "description": "POTATO production x999 - Strong boost",
    },
    "Better-er Land Button": {
        "cost": 30,
        "type": "INDUSTRY",
        "multiplier": 999,
        "boost": "Land",
        "priority": 7,
        "description": "LAND production x999 - Strong boost",
    },
    "Better-er Weapon Button": {
        "cost": 30,
        "type": "INDUSTRY",
        "multiplier": 999,
        "boost": "Weapons",
        "priority": 7,
        "description": "WEAPONS production x999 - Strong boost",
    },
    "Better-er Ore Button": {
        "cost": 30,
        "type": "INDUSTRY",
        "multiplier": 999,
        "boost": "Ore",
        "priority": 7,
        "description": "ORE production x999 - Strong boost",
    },
    "Better-er Medicine Button": {
        "cost": 30,
        "type": "INDUSTRY",
        "multiplier": 999,
        "boost": "Medicine",
        "priority": 7,
        "description": "MEDICINE production x999 - Strong boost",
    },
    # Temporary boosts (TRIALS tab) - Lower priority
    "Comrade Blast": {
        "cost": 5,
        "type": "TRIALS",
        "multiplier": 7777,
        "boost": "Comrades",
        "priority": 3,
        "description": "Comrade boost x7777 for 30 seconds - temporary",
    },
    "Potato Button Blast": {
        "cost": 10,
        "type": "TRIALS",
        "multiplier": 7777,
        "boost": "Potato",
        "priority": 4,
        "description": "Potato button x7777 for 20 seconds - temporary",
    },
    "Land Button Blast": {
        "cost": 10,
        "type": "TRIALS",
        "multiplier": 7777,
        "boost": "Land",
        "priority": 4,
        "description": "Land button x7777 for 20 seconds - temporary",
    },
    "Ore Button Blast": {
        "cost": 10,
        "type": "TRIALS",
        "multiplier": 7777,
        "boost": "Ore",
        "priority": 4,
        "description": "Ore button x7777 for 20 seconds - temporary",
    },
    "Weapon Button Blast": {
        "cost": 10,
        "type": "TRIALS",
        "multiplier": 7777,
        "boost": "Weapons",
        "priority": 4,
        "description": "Weapons button x7777 for 20 seconds - temporary",
    },
    "Medicine Button Blast": {
        "cost": 10,
        "type": "TRIALS",
        "multiplier": 7777,
        "boost": "Medicine",
        "priority": 4,
        "description": "Medicine button x7777 for 20 seconds - temporary",
    },
    # Resource surges (STATE tab) - Temporary
    "Big Resource Surge": {
        "cost": 50,
        "type": "STATE",
        "multiplier": "Instant",
        "boost": "Resources",
        "priority": 2,
        "description": "Get 4 hours worth of resources instantly",
    },
    "Mega Resource Surge": {
        "cost": 150,
        "type": "STATE",
        "multiplier": "Instant",
        "boost": "Resources",
        "priority": 1,
        "description": "Get 24 hours worth of resources instantly",
    },
}

# Known researched experiments
# The save file doesn't store which specific experiments you own, only the count.
# Manually update this list with experiments you've already researched to get accurate recommendations.
# Check in-game under EXPERIMENTS > INDUSTRY/STATE/TRIALS tabs to see which ones show as "RESEARCHED"
KNOWN_RESEARCHED = [
    # Example: "Best-est Potato Button",
    # Example: "Button Auto-Clickers",
]


def calculate_experiment_roi(
    experiment_name, experiment_data, current_scientists, current_production
):
    """
    Calculate ROI for an experiment.
    For permanent multipliers: ROI = multiplier / cost
    For temporary boosts: ROI is lower due to one-time use
    """
    cost = experiment_data["cost"]

    if cost > current_scientists:
        return None  # Can't afford

    multiplier = experiment_data.get("multiplier", 1)
    exp_type = experiment_data["type"]
    priority = experiment_data["priority"]

    # Calculate ROI score
    if isinstance(multiplier, (int, float)):
        # Permanent multipliers are MUCH more valuable
        if exp_type == "INDUSTRY":
            roi_score = (multiplier / cost) * priority
        else:
            # Temporary boosts are worth less
            roi_score = (multiplier / cost) * priority * 0.01
    else:
        # Special cases like auto-clickers or surges
        roi_score = priority * 100 / cost

    return {
        "name": experiment_name,
        "cost": cost,
        "type": exp_type,
        "multiplier": multiplier,
        "boost": experiment_data["boost"],
        "priority": priority,
        "description": experiment_data["description"],
        "roi_score": roi_score,
        "affordable": cost <= current_scientists,
    }


def analyze_experiments(decoded_data, researched_experiments=None):
    """
    Analyze all experiments and rank by ROI.
    Returns recommendations sorted by value.
    """
    if not decoded_data or "mission_progress" not in decoded_data:
        return [], 0

    # Get current scientists
    current_scientists = 0
    if "cards" in decoded_data:
        for card_id, card_data in decoded_data["cards"].items():
            if card_id == 36:  # Scientists currency
                current_scientists = int(card_data.get("value", 0))
                break

    # Get current production levels (for context and tiebreaker)
    current_production = {}
    if "cards" in decoded_data:
        resource_map = {1: "Potato", 2: "Land", 3: "Weapons", 4: "Ore", 5: "Medicine"}
        for card_id, name in resource_map.items():
            if card_id in decoded_data["cards"]:
                current_production[name] = decoded_data["cards"][card_id].get(
                    "value", 0
                )

    # Industry priority for tiebreaking (weakest first)
    # Medicine > Weapons > Ore > Land > Potato
    industry_priority = {
        "Medicine": 5,
        "Weapons": 4,
        "Ore": 3,
        "Land": 2,
        "Potato": 1,
        "Comrades": 0,
        "Resources": 0,
        "Passive": 0,
    }

    if researched_experiments is None:
        researched_experiments = KNOWN_RESEARCHED

    recommendations = []

    # Analyze each experiment
    for exp_name, exp_data in EXPERIMENTS.items():
        # Skip if already researched
        if exp_name in researched_experiments:
            continue

        roi = calculate_experiment_roi(
            exp_name, exp_data, current_scientists, current_production
        )
        if roi:
            # Add industry priority for tiebreaking
            roi["industry_priority"] = industry_priority.get(roi["boost"], 0)
            recommendations.append(roi)

    # Sort by ROI score (highest first), then by industry priority (weakest industry first)
    recommendations.sort(
        key=lambda x: (x["roi_score"], x["industry_priority"]), reverse=True
    )

    return recommendations, current_scientists


def format_experiment_recommendations(recommendations, current_scientists, top_n=15):
    """Format experiment recommendations as readable text."""
    if not recommendations:
        return "No experiments available or you can't afford any."

    output = []
    output.append(f"Current Scientists: {current_scientists:,}\n")
    output.append(f"{'='*90}")
    output.append(f"TOP {min(top_n, len(recommendations))} EXPERIMENT RECOMMENDATIONS")
    output.append(f"{'='*90}")
    output.append("")
    output.append("NOTE: To filter out experiments you already own, update the KNOWN_RESEARCHED")
    output.append("list in experiments_roi.py with the names of experiments you've researched.")
    output.append("")

    affordable = [r for r in recommendations if r["affordable"]]
    unaffordable = [r for r in recommendations if not r["affordable"]]

    if affordable:
        output.append("✅ AFFORDABLE NOW:\n")
        for i, rec in enumerate(affordable[:top_n], 1):
            mult_str = (
                f"x{rec['multiplier']:,}"
                if isinstance(rec["multiplier"], (int, float))
                else rec["multiplier"]
            )
            output.append(f"{i}. {rec['name']}")
            output.append(f"   Type: {rec['type']} | Industry: {rec['boost']}")
            output.append(f"   Cost: {rec['cost']:,} Scientists")
            output.append(f"   Effect: {mult_str}")
            output.append(
                f"   Priority: {'⭐' * rec['priority']} ({rec['priority']}/10)"
            )
            output.append(f"   ROI Score: {rec['roi_score']:,.2f}")
            output.append(f"   → {rec['description']}")
            output.append("")

    if unaffordable and len(affordable) < top_n:
        output.append(f"\n❌ NEED MORE SCIENTISTS:\n")
        remaining = top_n - len(affordable)
        for i, rec in enumerate(unaffordable[:remaining], len(affordable) + 1):
            mult_str = (
                f"x{rec['multiplier']:,}"
                if isinstance(rec["multiplier"], (int, float))
                else rec["multiplier"]
            )
            output.append(
                f"{i}. {rec['name']} - Need {rec['cost'] - current_scientists} more Scientists"
            )
            output.append(
                f"   Cost: {rec['cost']:,} | Effect: {mult_str} | Priority: {rec['priority']}/10"
            )
            output.append("")

    # Best by category
    output.append(f"\n{'='*90}")
    output.append("BEST EXPERIMENT BY CATEGORY")
    output.append(f"{'='*90}\n")

    best_by_type = {}
    for rec in recommendations:
        if rec["type"] not in best_by_type and rec["affordable"]:
            best_by_type[rec["type"]] = rec

    for exp_type in ["INDUSTRY", "STATE", "TRIALS"]:
        if exp_type in best_by_type:
            rec = best_by_type[exp_type]
            mult_str = (
                f"x{rec['multiplier']:,}"
                if isinstance(rec["multiplier"], (int, float))
                else rec["multiplier"]
            )
            status = "✅ AFFORDABLE" if rec["affordable"] else "❌ TOO EXPENSIVE"
            output.append(
                f"{exp_type:12} - {rec['name']:30} | {mult_str:12} | {rec['cost']:3} Scientists | {status}"
            )

    # Strategy tip
    output.append(f"\n{'='*90}")
    output.append("💡 STRATEGY TIP")
    output.append(f"{'='*90}")
    output.append(
        "1. INDUSTRY experiments (x99999, x9999, x999) are PERMANENT - highest priority!"
    )
    output.append(
        "2. When ROI is equal, recommendations prioritize your weakest industries"
    )
    output.append(
        "3. Focus on weakest industries (Medicine → Weapons → Ore → Land → Potato)"
    )
    output.append("4. Button Auto-Clickers is extremely valuable - saves tons of time")
    output.append(
        "5. TRIALS/STATE experiments are temporary - only buy when needed for missions"
    )
    output.append("6. Save Scientists for the big permanent multipliers when possible")

    return "\n".join(output)


def get_industry_production_ranking(decoded_data):
    """Rank industries by current production to suggest focus areas."""
    if "cards" not in decoded_data:
        return {}

    resource_map = {1: "Potato", 2: "Land", 3: "Weapons", 4: "Ore", 5: "Medicine"}
    production = {}

    for card_id, name in resource_map.items():
        if card_id in decoded_data["cards"]:
            production[name] = decoded_data["cards"][card_id].get("value", 0)

    # Sort by production (lowest first = weakest industry)
    ranked = sorted(production.items(), key=lambda x: x[1])
    return dict(ranked)
