SHMUP-GAME

This is a 2D space shooter game where the player controls a spaceship and tries to destroy falling meteors. 
The goal is to survive as long as possible and achieve the highest score by shooting down obstacles in space. 
The gameplay is simple but includes visual effects, sound, and power-ups to make it more dynamic.

Features

- Spaceship movement using keyboard controls
- Randomly generated meteors falling from the top
- Shooting bullets to destroy meteors
- Score tracking
- Health system
- Power-ups (shields, bombs, etc.)
- Explosion animations
- Background music and sound effects

Technologies Used

- Python 3
- Pygame (for graphics, sounds, and game logic)

What I Learned

- How to use Pygame to build a full game
- Managing a game loop and handling keyboard input
- Collision detection and shooting mechanics
- Adding and organizing images and sounds
- Structuring a project with multiple asset folders



This was one of my first more advanced game projects. It helped me build a stronger understanding of how real games work, both visually and technically.



FLAPPY-BIRD-GAME



This is a 2D side-scrolling game where the player controls a bird that must fly between obstacles (pipes).
The goal is to survive as long as possible and get the highest score. 
The game includes animations, background movement, collision detection, and scoring system.

Features

-Bird movement with spacebar
-Animated flapping using multiple bird images
-Randomly generated top and bottom pipes
-Score increases every time the bird passes a pipe
-Collision with pipe or ground ends the game
-Game over screen with final score
-Scrolling background and ground

Technologies Used
-Python 3
-Pygame (for graphics, input handling, and game logic)

What I Learned
-How to use Pygame to build a 2D game
-Creating game loops and managing events
-How to animate characters using images
-Collision detection between objects
-How to structure game assets like images in folders
-Improving overall understanding of how side-scrolling games work

JUMPER-GAME

This is a side-scrolling platform game where the player controls a character that runs forward, jumps over enemies, and collects bonus items to increase score. 
The goal is to avoid obstacles and survive as long as possible.

Features

-Player character with walking and jumping animations
-Gravity and jump mechanics using spacebar or mouse click
-Animated enemies (snails and flies) appear randomly
-Bonus item (gold bolt) gives extra score
-Background music and jump sound
-Game intro and game over screen with score display
-Uses pygame.sprite classes for better game structure

Technologies Used

-Python 3
-Pygame (for animations, input, sprite groups, sound, etc.)

What I Learned

-How to use object-oriented programming with Pygame
-Creating animated enemies and managing multiple sprites
-Using timers for generating enemies and animations
-Handling collisions between player, enemies, and bonuses
-Managing game states like start, active, and game over
-Sound effects and background music in games
-Improving code structure using pygame.sprite.Sprite classe

WEATHER-APP
This is a simple GUI application built using PyQt5 that shows the current weather of any city you input. 
It fetches real-time data from the OpenWeatherMap API and displays temperature, description, and an emoji representing the weather condition.

Features
-GUI layout with PyQt5
-User input for city name
-Connects to OpenWeatherMap API
-Shows temperature in Celsius
-Displays weather condition with text and emoji
-Error handling for various HTTP and connection errors
-Styled UI with Qt stylesheet

Technologies Used
-Python 3
-PyQt5 (for GUI components and styling)
-Requests (to handle API communication)
-OpenWeatherMap API

What I Learned
-Building user interfaces with PyQt5
-Working with layouts and custom widget styling
-Making HTTP requests with requests module
-Handling API responses and error codes
-Mapping weather codes to emojis for visualization
-Organizing code with object-oriented principles

FitTrack - Fitness Tracking and Visualization App
FitTrack is a desktop application that lets users log workout details and visualize fitness progress over time. 
You can enter the date, calories burned, distance ran, and a short description. 
Data is stored in an SQLite database and shown in a table view, with an option to display a scatter plot graph.

Main Features:
-Add and delete workouts
-View workout entries in a table
-Draw scatter plot showing distance vs calories
-Dark mode toggle
-Basic error handling
-Uses SQLite for data storage

Database Structure:
-The database is named fitness.db, with one table called fitness containing:
-id (integer, primary key)
-date (text)
-calories (real)
-distance (real)
-description (text)

Technologies used: 
-Python
-PyQt5 
-SQLite 
-Matplotlib

How it works:
You fill in the form with workout data and click “Add” to store it. 
The table updates automatically. “Delete” removes the selected workout. 
The “Submit” button creates a scatter plot showing how distance relates to calories burned.

What I learned:

This project helped me practice GUI design with PyQt5, including layout management, database connection with SQLite, and embedding matplotlib charts into a PyQt5 app. 
I also worked with input validation and simple database queries.
