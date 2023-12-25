# Copyright (c) 2023 Milford Gover

#This program is free software: you can redistribute it and/or modify it under the terms of the 
#GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
#without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 

class Sheath:
    def __init__(self):
        #create handling for case of Sheath already created
        #for now, assume new Sheath
        self.state_names = []
        self.states = {}
        #this list contains the many permutations of state transitions within the state machine tree
        self.list_of_paths = [] 

    def add(self, state_name, transition_state, transition_function, args = None):
        '''
        Add a transition to a new state from a current state.
        If this transition already is defined, this will replace the already exisiting one.

        Parameters:
        - state_name: The name of the state you want to transition FROM.
        - transition_state_name: The name of the state you want to transition TO.
        - transition_function: Function that would accomplish this transition from state_name to transition_state_name.

        Returns:
        None
        '''
        if args is None:
            args = []   #make args an empty list here. We don't this by default in the parameter list
                        #because we don't want defaults to be mutable types
        if transition_state not in self.state_names:
            self.state_names.append(transition_state)
        if state_name not in self.states:
            self.state_names.append(state_name)
            #add new state transition to dictionary of states, as a dictionary
            import pdb; pdb.set_trace()
            self.states[state_name] = {transition_state: lambda: transition_function(*args)}
        else:
            #current state already defined. must append
            self.states[state_name][transition_state] = lambda: transition_function(*args)
        
    def remove(self, state_name, transition_state):
        '''
        Removes the transition between a current state and goal state

        Parameters:
        - state_name: The name of the state you want to transition FROM.
        - transition_state_name: The name of the state you want to transition TO.

        Returns:
        True if transition was found and removed successfully
        False if transition could not be found and therefore NOT removed
        '''
        if state_name not in self.state_names:
            print("State {} not in list of states".format(state_name))
            return False
        else:
            if transition_state in self.states[state_name]:
                self.states[state_name] = None
            else:
                print("Transition between State {} to State {} not found".format(state_name, transition_state))
                return False
        return True
    
    def run(self, start_state, reset_function = None, args = None):
        '''
        Runs through every permutation of states using DFS. From start state to end states

        Parameters:
        - start_state: name the state which will be considered the starting state of the state machine
        - reset_function: a function which can bring the machine back to start state, at any point

        Retruns:
        None
        '''
        if args is None:
            args = []
        self._find_all_paths(start_state)
        for path in self.list_of_paths:
            for current_state_index in range(len(path)-1):
                current_state_name = path[current_state_index]
                next_state_name = path[current_state_index+1]

                #get the "subtree" where current state is root
                current_state = self.states[current_state_name]
                #get fuction that will take us from root to next state
                next_state_transition_function = current_state[next_state_name]
                next_state_transition_function()
        
            if reset_function is not None:
                print("path performed {}".format(path))
                print("performing reset function")
                reset_function(*args)

    def _find_all_paths_util(self, current, visited, path):
        #This is a recursive function to help find all
        #paths between start and end
        #This function utilize depth first search
        #mark this state as visited
        visited[current]=True
        path.append(current)

        #found end to a complete path
        #or move on with dfs
        if current not in self.states:
            self.list_of_paths.append(path[:])
        else:
            #continue dfs for this state
            for adjacent_state in self.states[current]:
                if visited[adjacent_state] == False:
                    self._find_all_paths_util(adjacent_state, visited, path) 

        #remove vertex from path and mark as unvisited
        path.pop()
        visited[current] = False

    def _find_all_paths(self, start):
        #This function will return a list of lists
        #each inner list will be a set of states between
        #start in end state, which describes a path
        #The outter list will contain all possible combinations 
        #of those paths
        visited = {}
        for state in self.state_names:
            visited[state] = False

        path = []
        self._find_all_paths_util(start, visited, path)