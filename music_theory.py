def string_to_camelot(key_string):
    camelot_wheel = {
        "C Major": "8B",
        "G Major": "9B",
        "D Major": "10B",
        "A Major": "11B",
        "E Major": "12B",
        "B Major": "1B",
        "F# / Gb Major": "2B",
        "C# / Db Major": "3B",
        "G# / Ab Major": "4B",
        "D# / Eb Major": "5B",
        "A# / Bb Major": "6B",
        "F Major": "7B",

        "C Minor": "5A",
        "G Minor": "6A",
        "D Minor": "7A",
        "A Minor": "8A",
        "E Minor": "9A",
        "B Minor": "10A",
        "F# / Gb Minor": "11A",
        "C# / Db Minor": "12A",
        "G# / Ab Minor": "1A",
        "D# / Eb Minor": "2A",
        "A# / Bb Minor": "3A",
        "F Minor": "4A",

        
    }
    return camelot_wheel.get(key_string, "Unknown")

# Function to convert pitch class and mode to string representation
def pitch_class_mode_to_string(pitch_class, mode):
    pitch_classes = ["C", "C# / Db",  "D", "D# / Eb", "E", "F", "F# / Gb", "G", "G# / Ab", "A", "A# / Bb", "B"]
    modes = ["Minor", "Major"]
    return pitch_classes[pitch_class] + " " + modes[mode]


def get_camelot_number(camelot_key):
    try:
        return int(camelot_key[:-1])
    except: 
        return "Unknown"
