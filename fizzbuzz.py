#!/usr/bin/env python3
"""
FizzBuzz Implementation

Requirements:
- Doorstop: REQ-001, REQ-002, REQ-003, REQ-004
- StrictDoc: REQ-001, REQ-002, REQ-003, REQ-004
"""

# REQ-001: Print numbers from 1 to 100
# REQ-002: Print Fizz for numbers divisible by three
# REQ-003: Print Buzz for numbers divisible by five
# REQ-004: Print FizzBuzz for numbers divisible by both three and five
for i in range(1, 101):
    if i % 15 == 0:
        # REQ-004: Print FizzBuzz for numbers divisible by both three and five
        print("FizzBuzz")
    elif i % 3 == 0:
        # REQ-002: Print Fizz for numbers divisible by three
        print("Fizz")
    elif i % 5 == 0:
        # REQ-003: Print Buzz for numbers divisible by five
        print("Buzz")
    else:
        # REQ-001: Print numbers from 1 to 100
        print(i)
