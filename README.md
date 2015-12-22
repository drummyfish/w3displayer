# w3-real-time-replay-info

This project implements simple tools to view real-time info about Warcraft III replays, as they are playing, which can be useful for game casters or just replay viewers.

The main tools is analyser, that analyses given replay and outputs a file with game states at given times. This file can then be played with one of multiple player.

Replay analysis cannot output some very useful data, such as current gold, lumber, whether a hero is dead or alive etc. - this would have to be done by accessing Warcraft III memory, which is unfortunatelly protected. Some basic info, such as heroes and their levels and abilities can be retrieved though.
