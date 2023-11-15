#include <stdio.h>
#include <stdlib.h>

#define MAX_CANDIDATES 2
#define MAX_VOTERS 10

// Structure to represent a candidate
struct Candidate {
    char name[50];
    int votes;
    char symbol;
    struct Candidate* next;
};

char symbolsForCandidates[5] = { '*', '@', '#', '$', '%' };
int symbolTaken[6];

// Structure for a voter choice node
struct VoterChoice {
    int choice;
    struct VoterChoice* next;
};

// Structure to represent a voter with an ID
struct Voter {
    int id;
    struct Stack* choices;
    struct Voter* next;
};

// Stack data structure to store voter choices
struct Stack {
    struct VoterChoice* top;
};

// Queue data structure to store votes
struct Queue {
    struct VoterChoice* front;
    struct VoterChoice* rear;
};

// Function to initialize candidates
void initializeCandidates(struct Candidate candidates[], int numCandidates) {
    for (int i = 0; i < numCandidates; i++) {
        printf("Enter the name of Candidate %d: ", i + 1);
        scanf("%s", candidates[i].name);

        printf("Choose Symbol for candidate: \n");
        printf("Available Symbols: \n");
        for (int j = 0; j < 5; j++) {
            if (symbolTaken[j] == 1)
                continue;
            printf("%d %c\n", j + 1, symbolsForCandidates[j]);
        }

        int num;
        printf("Enter the Symbol for Candidate %s: ", candidates[i].name);
        scanf("%d", &num);

        if (num <= 0 || num > 10 || symbolTaken[num - 1] == 1) {
            printf("This Symbol is not available. Please "
                   "choose from the available symbols\n");
            num = 0;
        } else {
            symbolTaken[num - 1] = 1;
            candidates[i].symbol = symbolsForCandidates[num - 1];
            candidates[i].votes = 0;
            candidates[i].next = NULL;
        }
    }
}
// Function to input and display voter IDs
int inputVoterID() {
    int voterID;
    printf("Enter your Voter ID (6 digits only): ");
    if (scanf("%d", &voterID) != 1 || voterID < 100000 || voterID > 999999) {
        printf("Invalid Voter ID. Please enter a 6-digit numeric ID.\n");
        // Clear the input buffer in case of invalid input
        while (getchar() != '\n');
        // Recursive call to retry input
        return inputVoterID();
    }
    return voterID;
}


void displayVoterID(int voterID) {
    printf("Your Voter ID is: %d\n", voterID);
}

// Function to push a choice onto the stack
void push(struct Stack* stack, int choice) {
    struct VoterChoice* newChoice = (struct VoterChoice*)malloc(sizeof(struct VoterChoice));
    newChoice->choice = choice;
    newChoice->next = stack->top;
    stack->top = newChoice;
}

// Function to pop a choice from the stack
int pop(struct Stack* stack) {
    if (stack->top) {
        int choice = stack->top->choice;
        struct VoterChoice* temp = stack->top;
        stack->top = stack->top->next;
        free(temp);
        return choice;
    }
    return -1; // Stack is empty
}

// Function to enqueue a vote
void enqueue(struct Queue* queue, int choice) {
    struct VoterChoice* newChoice = (struct VoterChoice*)malloc(sizeof(struct VoterChoice));
    newChoice->choice = choice;
    newChoice->next = NULL;
    if (queue->rear) {
        queue->rear->next = newChoice;
    } else {
        queue->front = newChoice;
    }
    queue->rear = newChoice;
}

// Function to dequeue a vote
int dequeue(struct Queue* queue) {
    if (queue->front) {
        int choice = queue->front->choice;
        struct VoterChoice* temp = queue->front;
        queue->front = queue->front->next;
        if (!queue->front) {
            queue->rear = NULL;
        }
        free(temp);
        return choice;
    }
    return -1; // Queue is empty
}

// Function to display the list of candidates
void displayCandidates(struct Candidate candidates[], int numCandidates) {
    printf("List of Candidates:\n");

    for (int i = 0; i < numCandidates; i++) {
        printf("%d. %s\n", i + 1, candidates[i].name);
        printf("Symbol : %c \n", candidates[i].symbol);
    }
}

// Function to display the vote count for each candidate
void displayResults(struct Candidate candidates[], int numCandidates) {
    printf("Election Results:\n");

    int maxVotes = 0;
    int winnerIndex = -1;
    int winnerFrequency = 0;
    for (int i = 0; i < numCandidates; i++) {
        if (candidates[i].votes > maxVotes) {
            maxVotes = candidates[i].votes;
            winnerIndex = i;
        }
    }

    for (int i = 0; i < numCandidates; i++) {
        if (candidates[i].votes == maxVotes) {
            winnerFrequency++;
        }
    }

    printf("\n-----RESULT-----\n");

    if (winnerFrequency > 1) {
        printf("No candidate has majority votes\n");
    } else if (winnerIndex != -1) {
        printf("The winner is: "
               "%s  \n with %d votes!\n",
               candidates[winnerIndex].name,
               maxVotes);
    } else {
        printf("No winner\n");
    }
}

int main() {
    struct Candidate candidates[MAX_CANDIDATES];
    struct Stack voterChoices;
    voterChoices.top = NULL;

    struct Queue voteQueue;
    voteQueue.front = NULL;
    voteQueue.rear = NULL;

    struct Voter* voters[MAX_VOTERS];
    int numVoters = 0;

    // Initialize candidates
    initializeCandidates(candidates, MAX_CANDIDATES);

    while (1) {
        printf("\nMain Menu:\n");
        printf("1. Display Candidates\n");
        printf("2. Cast Vote\n");
        printf("3. Display Results\n");
        printf("4. Exit\n");

        int choice;
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                displayCandidates(candidates, MAX_CANDIDATES);
                break;
            case 2: {
                int voterID = inputVoterID();
                displayVoterID(voterID);

                // Check if the voter has already voted
                int alreadyVoted = 0;
                for (int i = 0; i < numVoters; i++) {
                    if (voters[i]->id == voterID) {
                        alreadyVoted = 1;
                        printf("You have already voted.\n");
                        break;
                    }
                }

                if (!alreadyVoted) {
                    displayCandidates(candidates, MAX_CANDIDATES);
                    int voteChoice;
                    printf("Enter the number of your chosen candidate: ");
                    scanf("%d", &voteChoice);

                    if (voteChoice >= 1 && voteChoice <= MAX_CANDIDATES) {
                        candidates[voteChoice - 1].votes++;
                        push(&voterChoices, voteChoice);
                        enqueue(&voteQueue, voteChoice);

                        // Add the voter to the list
                        struct Voter* newVoter = (struct Voter*)malloc(sizeof(struct Voter));
                        newVoter->id = voterID;
                        newVoter->choices = &voterChoices;
                        newVoter->next = NULL;

                        voters[numVoters++] = newVoter;

                        printf("You've successfully cast your vote for %s!\n", candidates[voteChoice - 1].name);
                        printf("%c", candidates[voteChoice - 1].symbol);
                    } else {
                        printf("Invalid choice. Please select a valid candidate.\n");
                    }
                }

                break;
            }
            case 3:
                displayResults(candidates, MAX_CANDIDATES);
                break;
            case 4:
                // Free dynamically allocated memory
                while (voterChoices.top) {
                    pop(&voterChoices);
                }
                while (voteQueue.front) {
                    dequeue(&voteQueue);
                }

                // Free voter memory
                for (int i = 0; i < numVoters; i++) {
                    free(voters[i]);
                }

                exit(0);
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}
