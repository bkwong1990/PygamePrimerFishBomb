# Introduction

A Pygame example where you control a plane that drops bombs on laser tanks. This is based on [Real Python's Pygame primer](https://realpython.com/pygame-a-primer/).

# Installation

* Install Python 3.8.0 and Pygame 2.0.0.dev6 (Google is your friend)
* Download the archive and extract it
* `python3 fish_bomber.py` to start the game

# Story

The Republic of Piefon and the Empire of X-Ception are at war, with both sides using state-of-the-art magitechnology. You are a republic soldier who has been assigned a mission to test a prototype plane against an endless army of the empire's Heaven Piercer tanks, even though you're part of the republic's ground forces rather than their aerial forces. The plane itself lacks any equipment other than a magitech fish cloning machine, with the fish being genetically modified to explode on impact. All your parachutes are anvils and your plane's landing mechanism is malfunctioning for some reason, so you're basically flying your own coffin

On an unrelated note, several months ago, you and your bomber crew were witnesses who testified against your commanding officer in a military trial, only for the officer to get off scot-free for their war crimes and get hailed as a hero by the government and media. On another unrelated note, all the other corroborating witnesses were assigned to similar missions, with some becoming the protagonists of other Pygame primer derivatives and others becoming the protagonists of Minesweeper clones.

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
* my_sprites.py: A python file containing Sprite subclasses that I defined.
* battle.py A python file containing code needed to run the main gameplay portion
* title.py: A python file containing code needed to run the title screen

# To-do list

* Add start screen
* Add a short synopsis
* Add a tutorial
* Add a fullscreen toggle option
* Add config screen
* Save config file
* Implement a way to record the top 5 scores
* Credits for assets
* Export the game to a convenient executable
* Release by Jan 10 2020
* Release candidate by Jan 9 2020
* Classify todo as P1 vs defer
