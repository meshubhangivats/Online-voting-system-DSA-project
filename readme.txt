Features:
1.Candidate Initialization: Users can input candidate names and choose symbols from a predefined set.
2.Voter Registration: Voters are assigned unique IDs, and the system prevents duplicate votes from the same ID.
3.Vote Casting: Voters can cast their votes for a candidate, and the program updates the vote count accordingly.
4.Election Results: The program displays the election results, including the winning candidate (if any) and whether there is a majority.

=>Compile the Code:
  gcc voting_system.c -o voting_system
=>Run the Program:
  a.exe
=>Main Menu:
  Enter options to display candidates, cast votes, display results, or exit the program.
How to Use:
1.Display Candidates:
  Choose option 1 to view the list of candidates along with their symbols.
2.Cast Vote:
  Choose option 2 to cast a vote by entering your voter ID and selecting a candidate.
3.Display Results:
  Choose option 3 to view the election results, including the winning candidate and vote distribution.
4.Exit:
  Choose option 4 to exit the program, freeing allocated memory.
Details about the code:
1.The program uses a stack to manage voter choices and a queue to store votes.
2.Symbols for candidates are chosen from a predefined array.
3.Duplicate votes from the same voter ID are prevented to ensure the integrity of the election.

