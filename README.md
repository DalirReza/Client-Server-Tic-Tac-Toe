# Networked Tic-Tac-Toe (Operating Systems Project)

This repository contains the implementation of a networked, two-player Tic-Tac-Toe game, developed as a project for an Operating Systems course. The primary goal was not just to create a game, but to apply fundamental OS and networking concepts to enable real-time gameplay between two remote players.

The project is built on a client-server architecture and comes in two flavors: a full Graphical User Interface (GUI) version and a lightweight Command-Line Interface (CLI) version.

---

### Core Concepts Demonstrated

This project serves as a practical application of the following OS and networking principles:

* **Client-Server Architecture:** The game operates on a server-client model where a central server manages the game state, validates moves, and relays information between the two connected players.
* **Socket Programming:** Uses TCP sockets to establish a reliable, connection-oriented communication channel between the server and each client.
* **Multithreading:** The server utilizes threads to handle multiple client connections concurrently, allowing it to manage a game session without blocking.
* **Synchronization:** Employs synchronization primitives (like mutexes or semaphores) on the server to prevent race conditions and ensure the integrity of the shared game board state when multiple threads are accessing it.

---

### Features

* Real-time, two-player gameplay over a local network or the internet.
* **Two Implementations:**
    * A rich **GUI version** for an intuitive user experience.
    * A simple **CLI version** for lightweight, terminal-based play.
* 3*3, 4*4 and 5*5 board implemetation
* A robust communication protocol to handle moves, game state updates, and win/draw conditions.
* Centralized game logic on the server to ensure fair play and state consistency.

---
