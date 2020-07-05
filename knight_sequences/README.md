Knight Sequences

Pictured below is a keypad:

A - B - C - D - E

F - G - H - I - J

K - L - M - N - O

_ - 1 - 2 - 3 - _

Note: _ is a blank.

We want to find all 10-key sequences that can be keyed into the keypad in the following manner:
- The initial keypress can be any of the keys.
- Each subsequent keypress must be a knight move from the previous keypress.  
- There can be at most 2 vowels in the sequence.

A knight move is made in one of the following ways:
1. Move two steps horizontally and one step vertically.
2. Move two steps vertically and one step horizontally.

There is no wrapping allowed on a knight move.

Write a program that prints the number of valid 10-key sequences on a single line to standard out.  
