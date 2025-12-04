/*
 * FizzBuzz Implementation
 *
 * Requirements:
 * - Doorstop: REQ-001, REQ-002, REQ-003, REQ-004
 * - StrictDoc: REQ-001, REQ-002, REQ-003, REQ-004
 */

#include <stdio.h>

int main(void) {
    /* REQ-001: Print numbers from 1 to 100 */
    /* REQ-002: Print Fizz for numbers divisible by three */
    /* REQ-003: Print Buzz for numbers divisible by five */
    /* REQ-004: Print FizzBuzz for numbers divisible by both three and five */
    for (int i = 1; i <= 100; i++) {
        if (i % 15 == 0) {
            /* REQ-004: Print FizzBuzz for numbers divisible by both three and five */
            printf("FizzBuzz\n");
        } else if (i % 3 == 0) {
            /* REQ-002: Print Fizz for numbers divisible by three */
            printf("Fizz\n");
        } else if (i % 5 == 0) {
            /* REQ-003: Print Buzz for numbers divisible by five */
            printf("Buzz\n");
        } else {
            /* REQ-001: Print numbers from 1 to 100 */
            printf("%d\n", i);
        }
    }
    return 0;
}

