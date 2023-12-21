#!/bin/bash

# run new_game.py in a loop and handle errors
while true; do
    python new_game.py
    if [ $? -eq 0 ]; then
        echo "Game exited normally"
        break
    else
        echo "Game exited with error, restarting"
    fi
done
```