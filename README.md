# Azerbaijani SymSpell Correction API

A fast and accurate spell checking and correction API for the Azerbaijani language, powered by SymSpell algorithm.

## About SymSpell Algorithm

SymSpell is a symmetric spelling correction algorithm that offers a significant performance advantage over other spell checking approaches. 

### How it Works

SymSpell generates all possible term variants within an edit distance of the input term and then does a simple dictionary lookup to find the correct spellings. The algorithm's key advantages are:

1. **Precalculation**: Instead of calculating edit distance at runtime, SymSpell generates all possible dictionary term variations during initialization.
2. **Lookup Speed**: The algorithm achieves O(1) complexity for dictionary lookups, compared to O(n) for linear search approaches.
3. **Space Efficiency**: Uses a prefix tree (trie) data structure to store term variants efficiently.

### Configuration Parameters

- `max_edit_distance_dictionary` (default: 2)
  - Defines the maximum edit distance for generating term variations
  - Higher values:
    - Pros: Catches more spelling errors
    - Cons: Increases memory usage and initialization time
    - Example: Setting to 3 would catch "oxxumaq" → "oxumaq" but also increases false positives
  - Lower values:
    - Pros: More precise corrections, faster initialization
    - Cons: Might miss some valid corrections
  - Recommended: Stay with default (2) unless you have specific requirements

- `prefix_length` (default: 7)
  - Controls the length of term prefixes used in the dictionary
  - Affects memory usage and lookup speed
  - Current setting (7) is optimal for Azerbaijani language

## Usage

### Server Setup

1. Install requirements:
```bash
pip install flask symspellpy uvicorn
```

2. Download or prepare the Azerbaijani frequency dictionary (default: frequency_dictionary_az_80k.txt):
```
və 18702331
bu 9862854
ki 8801594
...
```

3. Run the server:
```bash
python app.py
```

### API Endpoint

Make GET requests to correct words:
```bash
curl "http://localhost:5000/correct?text=gedirem"
```

Response format:
```json
{
    "suggestions": [
        {
            "term": "gedirəm",
            "distance": 1,
            "count": 8661
        }
    ]
}
```

### Text Processing Utility

Here's a utility function to process entire texts while preserving format and case:

```python
import requests
import re

def correct_text(text, api_url="http://localhost:5000/correct"):
    # Split text into words while preserving separators
    parts = re.split(r'(\W+)', text)
    
    corrected_parts = []
    for part in parts:
        # Skip empty parts and non-word characters
        if not part or not part.strip() or not re.match(r'\w+', part):
            corrected_parts.append(part)
            continue
            
        # Make API request
        response = requests.get(f"{api_url}?text={part.lower()}")
        if response.status_code == 200:
            data = response.json()
            if data.get('suggestions'):
                correction = data['suggestions'][0]['term']
                # Preserve original case
                if part.isupper():
                    correction = correction.upper()
                elif part[0].isupper():
                    correction = correction.capitalize()
            else:
                correction = part
        else:
            correction = part
            
        corrected_parts.append(correction)
    
    return ''.join(corrected_parts)

# Usage example
text = "Mən Bakiya gedirem!"
corrected = correct_text(text)
print(corrected)  # Output: "Mən Bakıya gedirəm!"
```

## About

### Authors
Developed by LocalDoc team.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

---
