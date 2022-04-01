## Delaying inside the game loop

```python
current_tick = 0
next_tick = 0

# inside the game loop
current_tick = pygame.time.get_ticks()
if current_tick > next_tick:
    next_tick += 200 # interval
    # do something you need to repeat slowly
```

## Heuristic ideas

- Basic: count `the number of fours - my opponent's fours`
- Count `the number of four steps you can go without being interrupted by an opponent's coin, the number of possible fours I can fill in the future - the same for my opponent`. It is redundant to count completely empty fours.  
    - But now there's no difference between a state with 4 coins in a row , and another with one coin and 3 empty spaces in a row.
    - we could replace the value of the state with empty spaces with an expected value instead, increasing this value with each filled space as you get a more solid chance at filling the fours in the future, this probability becomes 1 when there are no empty spaces. meaning:
    > Assuming a 50 % chance of the opponent filling the space: 
    >
    > We will score a point 50 % of the time so 
    > $ h_1 = 0.5 * (+1) $ 
    >
    > and will not score a point 50 % so 
    > $h_2 = 0.5 * (0)$.
    >
    > Now $h = 0.5 * x + 0.5 * (x - 1)$.
    > where $x$ is the score.
    >
    > This may be too pessimistic to be admissible (50% chance of failure for each node).
    >
    > Since we want to stay optimistic (admissible) and since there is no way to simulate the opponent's optimal method of thinking without completing the search tree, we will assume a uniformly distributed probability function for the opponent's next move.
    >
    > Assuming $p(fail) = (\frac{1}{C} * \frac{C - 1}{C} ^{C - 1}) $ chance of failure for each single empty space.$= around\ 0.057$ for $C = 7$ where $C$ is the number of non-full columns. 
    >
    > Knowing that the failure of any single empty space of the state will lead to its failure: $P_{state failure} = n p(fail)$ where $n$ is the number of empty spaces in a row.
    >
    > $maximum\ p_{state failure}\ |_{n = 4} = 0.228$ for $C = 7$
    >
    > $h = (1 - np(fail)) * x + np(fail) * (x - 1)$
    >
    > this heuristic is admissible for a Max node. May a Min node use it ?
    >
    > this works for fours in a row, does it work for columns and diagonals?

## regex for string representation checks:

    