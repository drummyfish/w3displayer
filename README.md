# w3displayer

This work-in-progress project implements simple tools to view real-time info about Warcraft III replays, as they are playing, which can be useful for game casters or just replay viewers. It even allows for limited replay viewing without the Warcraft III game.

The main tool is the analyser, which analyses given replay file and outputs a file with game states at given times. This file can then be played with one of multiple players.

Due to the replay format nature, replay analysis can not unfortunately easily output some very useful data, such as current gold, lumber, whether a hero is dead or alive etc. - this would have to be done by hacking into Warcraft III memory, which is unfortunatelly protected. Some info can however be retrieved, such as:

- Player info - names, races, teams, ...
- Heroes\*, their levels\*, abilities\*, ability levels\*, whether an ability has been recently used.
- APM
- recent actions (such as trained units, buildings, item uses etc.)
- Current tier\*
- Approximate resources (gold, lumber, food) spent.\*
- Approximate number of units and buildings.\*
- Number of expansions\*
- ...

\*: potentially not accurate 100% of the time, but mostly correct

an early demo:

[![video](http://img.youtube.com/vi/6FCSJNOZixk/0.jpg)](http://www.youtube.com/watch?v=6FCSJNOZixk "video")

usage
-----

```
python analyse.py replay.w3g > replay.txt
```

Then you can for example play the replay with console player:

```
python console_player.py replay.txt
```

Or with JavaScript player by opening javascript_player.html in your browser (Chrome) and loading the replay.txt.
