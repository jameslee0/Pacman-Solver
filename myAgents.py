#James Lee
#RedID: 820655947
#Class: CS550-01-02
#Due Date: 09/02/2021
from pacman import Directions
from game import Agent, Actions
from pacmanAgents import LeftTurnAgent

#I promise that the attached assignment is my own work. I recognize that should this not be the case, 
#I will be subject to penalties as outlined in the course syllabus. James Lee
class TimidAgent(Agent):
    """
    A simple agent for PacMan
    """

    def __init__(self):
        super().__init__()  # Call parent constructor
        # Add anything else you think you need here

    def inDanger(self, pacman, ghost, dist=3):
        """inDanger(pacman, ghost) - Is the pacman in danger
        For better or worse, our definition of danger is when the pacman and
        the specified ghost are:
           in the same row or column,
           the ghost is not scared,
           and the agents are <= dist units away from one another

        If the pacman is not in danger, we return Directions.STOP
        If the pacman is in danger we return the direction to the ghost.
        """

        # Your code

        #This is where I will apply variables to find the position of the ghost and pacman in terms of rows and columns
        ghostRowPlacement = ghost.getPosition()[0]
        ghostColumnPlacement = ghost.getPosition()[1]
        pacRowPlacement = pacman.getPosition()[0]
        pacColumnPlacement = pacman.getPosition()[1]

        #This will essentially check to see that if pacman and the ghosts aren't in the same row or column, it will default to Directions.STOP
        if pacColumnPlacement != ghostColumnPlacement and pacRowPlacement != ghostRowPlacement:
            return Directions.STOP

        #Had code to check the abs value of rowDistance and columnDistance and if its in the range of 3 it will call Directions.STOP but it didn't seem needed.

        #If the pacman and ghost share the same column it will run this code.
        if pacColumnPlacement == ghostColumnPlacement:
            #Calculates the distance subtracting the row coordinates because they are on the same column so must use row placement to find distance.
            rowDistance = pacRowPlacement-ghostRowPlacement
            #This will check if the distance is within our limit range of 3, and if it's above 0 we know that the ghost is West of pacman.
            if rowDistance <= dist and not ghost.isScared() and rowDistance > 0:
                return Directions.WEST
            #This will check if the distance is within our limit range of 3, and if it's less than 0 we know that the ghost is East of pacman.
            elif rowDistance <= dist and not ghost.isScared() and rowDistance < 0:
                return Directions.EAST
            #If the ghost is not in range, pacman will keep going in its direction and call Directions.STOP
            else:
                return Directions.STOP
        
        #If the pacman and ghost share the same row it will run this code.
        if pacRowPlacement == ghostRowPlacement:
            #Calculates the distance subtracting the column coordinates because they are on the same row so must use column placement to find distance.
            columnDistance = pacColumnPlacement-ghostColumnPlacement
            #This will check if the distance is within our limit range of 3, and if it's above 0 we know that the ghost is South of pacman.
            if columnDistance <= dist and not ghost.isScared() and columnDistance > 0:
                return Directions.SOUTH
            #This will check if the distance is within our limit range of 3, and if it's above 0 we know that the ghost is North of pacman.
            elif columnDistance <= dist and not ghost.isScared() and columnDistance < 0:
                return Directions.NORTH
            #If the ghost is not in range, pacman will keep going in its direction and call Directions.STOP
            else:
                return Directions.STOP

        #If pacman and the ghost are not in the same row or column, call Directions.STOP
        else:
            return Directions.STOP

        raise NotImplemented
    
    def getAction(self, state):

        # List of directions the agent can choose from
        legal = state.getLegalPacmanActions()

        # Get the pacman's and the ghosts' state from the game state and find pacman heading
        pacmanState = state.getPacmanState()
        ghostStates = state.getGhostStates()
        heading = pacmanState.getDirection()

        if heading == Directions.STOP:
            # Pacman is stopped, assume North (true at beginning of game)
            heading = Directions.NORTH

        #Loops to see if any of the ghosts in ghostStates are currently a threat to pacman. Must loop because there are more than one ghost.
        for ghost in ghostStates:
            pacmanInDanger = self.inDanger(pacmanState, ghost)

        #If pacmanInDanger gives a specific direction other than Directions.STOP call this code to tell pacman which direction to go.
        if pacmanInDanger != Directions.STOP:
            #The first check should be to see if pacman can reverse its direction by checking to see if it is in its legal moves.
            if Directions.REVERSE[pacmanInDanger] in legal:
                action = Directions.REVERSE[pacmanInDanger]
            #The second check should be to see if pacman can turn left from its current heading by checking to see if it is in its legal moves.
            elif Directions.LEFT[pacmanInDanger] in legal:
                action = Directions.LEFT[pacmanInDanger]
            #The third check should be to see if pacman can turn right from its current heading by checking to see if it is in its legal moves.
            elif Directions.RIGHT[pacmanInDanger] in legal:
                action = Directions.RIGHT[pacmanInDanger]
            #If those directions are all not in legal, we will keep going towards the danger as that is our only option.
            elif pacmanInDanger in legal:
                action = Directions.pacmanInDanger
            else:
                action = Directions.STOP
        
        #If the pacmanInDanger doesn't call for immediate danger, run the LeftTurnAgent code.
        else:
            # Turn left if possible
            left = Directions.LEFT[heading]  # What is left based on current heading
            if left in legal:
                action = left
            else:
                # No left turn
                if heading in legal:
                    action = heading  # continue in current direction
                elif Directions.RIGHT[heading] in legal:
                    action = Directions.RIGHT[heading]  # Turn right
                elif Directions.REVERSE[heading] in legal:
                    action = Directions.REVERSE[heading]  # Turn around
                else:
                    action = Directions.STOP  # Can't move!

        return action
