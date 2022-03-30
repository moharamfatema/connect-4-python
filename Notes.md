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

- Basic: count the number of fours - my opponent's fours
- Count the number of four steps you can go without being interrupted by an opponent's coin, the number of possible fours I can fill in the future - the thame for my opponent. It is redundant to count completely empty fours.