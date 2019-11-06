// Agent.cc

#include <iostream>
#include <cstdio>
#include "Agent.h"
#include "Orientation.h"

using namespace std;

const int size = 5;

double pitChance[size][size];

int x = 0, y =0;

Orientation o;

class Orientation

Agent::Agent ()
{
    o = Orientation.Right;
    printf("Constructor");
	for (auto &i : pitChance) {
		for (double &j : i) {
			j = .2;
		}
	}
}

Agent::~Agent ()
{
    printf("Destruct");
}

void Agent::Initialize ()
{
    printf("Initialize");

}

bool outOfBounds(int x, int y){
    return x < 0 || x >= size || y < 0 || y >= size;
}

void findBestNeighbor(int *xRes, int *yRes){
    int nX[] = {x - 1, x - 1, x + 1, x + 1};
    int nY[] = {y - 1, y + 1, y - 1, y + 1};

    double lowestAccpetable = 1;
    double acceptableIndex = -1;

    for(int i = 0; i < 4; i++){
        if(outOfBounds(nX[i], nY[i])){
            continue;
        }

        int curPitChance = pitChance[nX[i]][nY[i]];


        if(lowestAccpetable > curPitChance && curPitChance < .5 && curPitChance > 0){

        }

    }
}

Action Agent::Process (Percept& percept)
{
	char c;
	Action action;
	bool validAction = false;

    pitChance[x][y] = 0;

	while (! validAction)
	{
		validAction = true;
		cout << "Action? ";
		cin >> c;
		if (c == 'f') {
			action = GOFORWARD;
		} else if (c == 'l') {
			action = TURNLEFT;
		} else if (c == 'r') {
			action = TURNRIGHT;
		} else if (c == 'g') {
			action = GRAB;
		} else if (c == 's') {
			action = SHOOT;
		} else if (c == 'c') {
			action = CLIMB;
		} else {
			cout << "Huh?" << endl;
			validAction = false;
		}
	}
	return action;
}

void Agent::GameOver (int score)
{

}

