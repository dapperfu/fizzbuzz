/*
 * FizzBuzz Implementation
 *
 * Requirements:
 * - Doorstop: REQ-001, REQ-002, REQ-003, REQ-004
 * - StrictDoc: REQ-001, REQ-002, REQ-003, REQ-004
 */

fn main() {
    // REQ-001: Print numbers from 1 to 100
    // REQ-002: Print Fizz for numbers divisible by three
    // REQ-003: Print Buzz for numbers divisible by five
    // REQ-004: Print FizzBuzz for numbers divisible by both three and five
    for i in 1..=100 {
        if i % 15 == 0 {
            // REQ-004: Print FizzBuzz for numbers divisible by both three and five
            println!("FizzBuzz");
        } else if i % 3 == 0 {
            // REQ-002: Print Fizz for numbers divisible by three
            println!("Fizz");
        } else if i % 5 == 0 {
            // REQ-003: Print Buzz for numbers divisible by five
            println!("Buzz");
        } else {
            // REQ-001: Print numbers from 1 to 100
            println!("{}", i);
        }
    }
}

