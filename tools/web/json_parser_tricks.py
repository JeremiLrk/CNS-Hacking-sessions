"""[EXTRA / PREVIOUS] JSON DUPLICATE KEYS and HMAC Vault.

WHY YOU SHOULD CARE:
Python's json.loads normally keeps the LAST value of a duplicate key.
Some OTHER software may use the FIRST value instead.
If authentication and permission checks disagree, a bug may happen.

This is NOT a cryptographic weakness in HMAC itself.
"""
import json


def last_value_wins(raw_json):
    return json.loads(raw_json)


def first_value_wins(raw_json):
    # Instead of normal parsing, we get pairs of key/value entries.
    # First key occurrence wins. (Only to SHOW parsing differences.)
    def first(pairs):
        result = {}
        for key, value in pairs:
            if key not in result:
                result[key] = value
        return result
    return json.loads(raw_json, object_pairs_hook=first)


def reject_double_keys(raw_json):
    # This is how a safety-conscious parser could reject ambiguous JSON.
    def no_duplicates(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("This JSON repeats key: " + key)
            result[key] = value
        return result
    return json.loads(raw_json, object_pairs_hook=no_duplicates)


if __name__ == "__main__":
    text = '{"action":"view","role":"admin","role":"user"}'
    print("First value wins:", first_value_wins(text))
    print("Last value wins:", last_value_wins(text))
    try:
        reject_double_keys(text)
    except ValueError as error:
        print("Rejected:", error)
    assert first_value_wins(text)["role"] == "admin"
    assert last_value_wins(text)["role"] == "user"
