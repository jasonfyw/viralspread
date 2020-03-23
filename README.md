# Viral Spread Simulation
*Simulating the spread of an infectious disease using collisions of moving circles*

*WP article for reference:* https://www.washingtonpost.com/graphics/2020/world/corona-simulator/

## viralspread.py
Sprite movement calculated by a scalar speed and an angle of travel.

*Currently not working properly due to buggy sprite collision*

## viralspread2.py

![](viralspread2_example_run.gif)

Sprite movement calculated by component velocities in the x and y planes.

Default of 1 initially infected person. Other people are infected on collision with an infected person.
