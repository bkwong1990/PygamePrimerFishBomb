# Introduction

A Pygame example where you control a plane that drops bombs on laser tanks. This is based on [Real Python's Pygame primer](https://realpython.com/pygame-a-primer/).

# Installation

* Install Python 3.8.0 and Pygame 2.0.0.dev6 (Google is your friend)
* This was developed and tested on macOS Catalina.
* Download the archive and extract it
* `python3 fish_bomber.py` to start the game

# Story

The Republic of Piefon and the Empire of X-Ception are at war, with both sides using state-of-the-art magitechnology. You are a republic soldier who has been assigned a mission to test a prototype plane against an endless army of the empire's Heaven Piercer tanks, even though you're part of the republic's ground forces rather than their aerial forces. The plane itself lacks any equipment other than a magitech fish cloning machine, with the fish being genetically modified to explode on impact. All your parachutes are anvils and your plane's landing mechanism is malfunctioning for some reason, so you're basically flying your own coffin.

On an unrelated note, several months ago, you and your bomber crew were witnesses who testified against your commanding officer in a military trial, only for the officer to get off scot-free for their war crimes and get hailed as a hero by the government and media. On another unrelated note, all the other corroborating witnesses and dissenting officers were assigned to similar missions, with some becoming the protagonists of other Pygame primer derivatives and others becoming the protagonists of Minesweeper clones. On a third unrelated note, the crew of the surprisingly fragile Heaven Piercer tanks are people who posted and shared unflattering memes about their emperor on social media.

# How to play

* Move with the arrow keys.
* Drop bomb with the spacebar. Beware of the four second reload time. Also beware of the slight forward drift of the bomb.
* Game Over if you're hit even once

## Scoring System

* Your score will increase over time and will increase more the faster the missiles move. Each active tank will increase your score even faster.
* Missiles and tanks can be destroyed by bombing them or if your plane collides with them. They're worth 1000 and 10000 pts respectively.
* The tank will shoot lasers, which can only be destroyed by bombs but will disappear in 1/6 of a second. They're worth 20000 pts.
* To get on the high score list, you must surpass the current 5th best score on the highest difficulty settings.

# Python Files

* fish_bomber.py : The python file to be executed in order to launch the game.
* my_events.py: A python file containing events that I defined along with related functions.
* my_sprites.py: A python file containing Sprite subclasses that I defined.
* my_menu.py: A python file containing code to draw a functioning menu
* battle_session.py: A python file containing code needed to run the main gameplay portion
* title_session.py: A python file containing code needed to run the title screen
* config_session.py: A python file allowing the user to adjust game settings
* config_helper.py: Includes functions to read and write the config.json file
* input_score_session.py: Gets keyboard input from the user to enter a name for their highscore
* view_scores_session.py: Shows a list of the top five scores
* score_helper.py: Includes functions to load and save high scores

# Credits

## Audio
* I personally recorded kailh_navy.ogg and reloaded.ogg
* 01_go_without_seeing_back_.ogg  
 * [Go Without Seeing Back by Makoto Saita](https://big-up.style/musics/34958?wovn=en)
* sorato.ogg
 * [Sora by Misaki Shin / G2-Midi](http://guru2.nobody.jp/music/town.htm)
* laser.ogg
 * [Laser Cannon by Mike Koenig](http://soundbible.com/1771-Laser-Cannon.html)
* explosion.ogg
 * [Bomb Exploding by Sound Explorer](http://soundbible.com/1986-Bomb-Exploding.html)
* ovation.ogg
 * [Ovation Sound by Mike Koenig](http://soundbible.com/1647-Ovation.html)

## Images
* I personally made spacebar.png and spacebar_no.png using a combination of Pixel Art Maker and GIMP.
* laser.png was made by me using GIMP
* keyboard.png was taken by my phone
* cloud.png
 * [Cloud Cartoon from cleanpng](https://www.cleanpng.com/png-cloud-computing-dust-676210/preview.html)
* config_background.png
 * [by Pixabay](https://www.pexels.com/photo/architect-architecture-blueprint-build-271667/)
* explosion.png
 * [Example Sprite Sheet Animation - Sprite Sheet Particle Unity
from pnglot](https://www.pnglot.com/i/hJJxmbR_example-sprite-sheet-animation-sprite-sheet-particle-unity/)
* fish_bomb.png
 * [2D Retro Fish by EXCITESZZ](https://opengameart.org/content/2d-retro-fish)
* jet.png
 * [Figther Jet by Juan Garces, ES ](https://thenounproject.com/term/fighter-jet/59845/)
* missile.png
 * [Missile No Background from Premium BP Themes](https://premiumbpthemes.com/explore/missile-transparent-background.html)
* newspaper.png
 * [by brotiN biswaS](https://www.pexels.com/photo/advertisements-batch-blur-business-518543/)
* tank.png
 * [Tank Sprite from Hunt PNG](https://huntpng.com/keyword/tank-sprite-png)
* title_background.png
 * [by Elia Clerici](https://www.pexels.com/photo/photo-of-blue-sky-912110/)
