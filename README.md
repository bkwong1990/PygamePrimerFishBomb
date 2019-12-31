# Introduction

A Pygame example where you control a plane that drops bombs on laser tanks. This is based on [Real Python's Pygame primer](https://realpython.com/pygame-a-primer/).

# Installation

* Install Python 3.8.0 and Pygame 2.0.0.dev6 (Google is your friend)
* Download the archive and extract it
* `python3 fish_bomber.py` to start the game

# How to play

* Move with the arrow keys.
* Drop bomb with the spacebar. Beware of the four second reload time.
* Press Z to lower the speed of the missiles at the cost of halving your score.
* Press X to increase the speed of the missiles.
* Game Over if you're hit even once

## Scoring System

* Your score will increase over time and will increase more the faster the missiles move.
* Missiles and tanks can be destroyed by bombing them or if your plane collides with them. They're worth 1000 and 10000 pts respectively.
* The tank will shoot lasers, which can only be destroyed by bombs but will disappear in 1/6 of a second. They're worth 20000 pts.

# Python Files

* fish_bomber.py : The python file to be executed in order to launch the game.
* my_events.py: A python file containing events that I defined along with related functions.
* my_sprites: A python file containing Sprite subclasses that I defined.

# To-do list

* Add on-screen key indicator for dropping the bomb
* Implement a way to record the top 5 scores
* Credits for assets
* Export the game to a convenient executable
