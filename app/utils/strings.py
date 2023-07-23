def reverse_string(s: str) -> str:
    return s[::-1]

def is_palindrome(s: str) -> bool:
    return s == s[::-1]