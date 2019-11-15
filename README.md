# 3D-Tic-Tac-Toe with Reinforcement Learning

## Environment:

Python 3.6 

## Training

This code trains 2 AI agents against each other for n1, n2, and n3 games respectively. The format for the command line input is:
```
python 3D_Tic_Tac_Toe.py -n1 250 -n2 500 -n3 1000
```
As a convention, n1 < n2 < n3. If no command line input is entered, the default values are set to n1=100, n2=500, and n3=2000.

## View Utility Values
The utility of each (state, action) is stored in a corresponding text file (example data dumps are included in this repo). These files can be printed to stdout using <TicTacToeInstance>.printQTables(<# of iterations>).
