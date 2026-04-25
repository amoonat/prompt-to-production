"""
UC-0A — Complaint Classifier
Implemented based on RICE → agents.md → skills.md
"""
import argparse
import csv

def classify_complaint(row: dict) -> dict:
    """
    Classify a single complaint row.
    Returns: dict with keys: complaint_id, category, priority, reason, flag
    """
    complaint_id = row.get("complaint_id", "UNKNOWN")
    description = row.get("description", "").strip()
    
    # Error handling from skills.md & agents.md
    if not description or len(description) < 5:
        return {
            "complaint_id": complaint_id,
            "category": "Other",
            "priority": "Low",
            "reason": "Description is missing or too short to classify.",
            "flag": "NEEDS_REVIEW"
        }
    
    desc_lower = description.lower()
    
    # Priority logic based on exact keywords
    urgent_keywords = ["injury", "child", "school", "hospital", "ambulance", "fire", "hazard", "fell", "collapse"]
    priority = "Standard"
    for kw in urgent_keywords:
        if kw in desc_lower:
            priority = "Urgent"
            break
            
    # Category mapping heuristics
    categories_map = {
        "Pothole": ["pothole", "crater"],
        "Flooding": ["flood", "waterlogging", "water", "drainage"],
        "Streetlight": ["light", "streetlamp", "dark", "bulb"],
        "Waste": ["waste", "garbage", "trash", "dump"],
        "Noise": ["noise", "loud", "music", "barking"],
        "Road Damage": ["road", "crack", "pavement"],
        "Heritage Damage": ["heritage", "monument", "statue"],
        "Heat Hazard": ["heat", "sun", "temperature"],
        "Drain Blockage": ["drain", "sewer", "clog", "blockage"]
    }
    
    matched_cat = "Other"
    matched_word = None
    
    for cat, keywords in categories_map.items():
        for kw in keywords:
            if kw in desc_lower:
                matched_cat = cat
                matched_word = kw
                break
        if matched_word:
            break
            
    if matched_cat == "Other":
        category = "Other"
        # Extract a snippet to cite
        snippet = description.split()[0] if description else "unknown"
        reason = f"Classified as Other because the description containing '{snippet}' did not match specific known categories."
        flag = "NEEDS_REVIEW"
    else:
        category = matched_cat
        reason = f"Classified as {category} because the description contains the word '{matched_word}'."
        flag = ""

    return {
        "complaint_id": complaint_id,
        "category": category,
        "priority": priority,
        "reason": reason,
        "flag": flag
    }


def batch_classify(input_path: str, output_path: str):
    """
    Read input CSV, classify each row, write results CSV.
    """
    results = []
    try:
        with open(input_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    classification = classify_complaint(row)
                    results.append(classification)
                except Exception as e:
                    print(f"Error processing row {row.get('complaint_id', 'UNKNOWN')}: {e}")
                    # Ensure output is still generated for failed rows
                    results.append({
                        "complaint_id": row.get("complaint_id", "UNKNOWN"),
                        "category": "Other",
                        "priority": "Low",
                        "reason": f"Row failed processing due to error: {str(e)}",
                        "flag": "NEEDS_REVIEW"
                    })
    except Exception as e:
        print(f"Failed to read input file: {e}")
        return

    if not results:
        print("No valid rows were processed. Creating an empty file.")
    
    fieldnames = ["complaint_id", "category", "priority", "reason", "flag"]
    try:
        with open(output_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    except Exception as e:
        print(f"Failed to write output file: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UC-0A Complaint Classifier")
    parser.add_argument("--input",  required=True, help="Path to test_[city].csv")
    parser.add_argument("--output", required=True, help="Path to write results CSV")
    args = parser.parse_args()
    batch_classify(args.input, args.output)
    print(f"Done. Results written to {args.output}")
