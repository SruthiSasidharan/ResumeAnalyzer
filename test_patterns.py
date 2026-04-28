import re

# Current patterns that aren't working
EDUCATION_PATTERNS_OLD = [
    r'(?i)\b(?:b\.?tech|b\.?e\.?|b\.?s\.?|b\.?sc|b\.?com|b\.?ca)\b\s*(?:in|–|-|:)?\s*([a-zA-Z\s&\-\.]{3,80}?)(?:\n|,|;|$|–)',
    r'(?i)\b(?:m\.?tech|m\.?e\.?|m\.?s\.?|m\.?sc|m\.?ba|m\.?ca)\b\s*(?:in|–|-|:)?\s*([a-zA-Z\s&\-\.]{3,80}?)(?:\n|,|;|$|–)',
    r'(?i)\b(?:bachelor|master|phd|doctoral|associate)\s+(?:degree|of)?\s*(?:in)?\s+([a-zA-Z\s&\-\.]{5,80}?)(?:\n|,|;|$|from)',
    r'(?i)\b(?:diploma|certification|certified)\b[:\s]+([a-zA-Z\s&\-\.]{5,80}?)(?:\n|,|;|$)',
    r'(?i)(?:graduated?|completed|passed)\s+(?:from|at)?\s+([a-zA-Z0-9\s\-\.&]{5,80}?)(?:\n|,|;|$)',
]

# Better patterns that don't require end-of-string
EDUCATION_PATTERNS_NEW = [
    r'(?i)b\.?tech\s+(?:in|–|-|:)?\s*([a-zA-Z0-9\s&\-\.(),]+?)(?=\n|$|,|;)',
    r'(?i)b\.?e\.?\s+(?:in|–|-|:)?\s*([a-zA-Z0-9\s&\-\.(),]+?)(?=\n|$|,|;)',
    r'(?i)b\.?s\.?\s+(?:in|–|-|:)?\s*([a-zA-Z0-9\s&\-\.(),]+?)(?=\n|$|,|;)',
    r'(?i)m\.?tech\s+(?:in|–|-|:)?\s*([a-zA-Z0-9\s&\-\.(),]+?)(?=\n|$|,|;)',
    r'(?i)m\.?e\.?\s+(?:in|–|-|:)?\s*([a-zA-Z0-9\s&\-\.(),]+?)(?=\n|$|,|;)',
    r'(?i)m\.?s\.?\s+(?:in|–|-|:)?\s*([a-zA-Z0-9\s&\-\.(),]+?)(?=\n|$|,|;)',
    r'(?i)bachelor\s+(?:of\s+technology|of\s+engineering|of\s+science|degree)?\s*(?:in)?\s*([a-zA-Z0-9\s&\-\.(),]+?)(?=\n|$|,|;)',
    r'(?i)master\s+(?:of\s+technology|of\s+engineering|of\s+science|degree)?\s*(?:in)?\s*([a-zA-Z0-9\s&\-\.(),]+?)(?=\n|$|,|;)',
    r'(?i)(?:phd|ph\.d|doctorate)\s+(?:in)?\s*([a-zA-Z0-9\s&\-\.(),]+?)(?=\n|$|,|;)',
]

test_text = """
Education:
B.Tech in Computer Science from NRI Institute
M.Tech in Machine Learning  
Bachelor of Technology in Information Technology, 2022
Master of Science in Data Science
Graduation: B.E. in Electronics Engineering
Diploma in Web Development
PhD in Artificial Intelligence
Completed B.Sc in Mathematics
Graduated from Anna University with B.Tech
"""

print("=" * 80)
print("TESTING NEW PATTERNS:")
print("=" * 80)

for i, pattern in enumerate(EDUCATION_PATTERNS_NEW):
    matches = list(re.finditer(pattern, test_text))
    if matches:
        print(f"\nPattern {i+1}: {pattern[:70]}...")
        for m in matches:
            group_text = m.group(1).strip() if m.lastindex and m.lastindex >= 1 else m.group(0)
            print(f"  ✓ {group_text}")
