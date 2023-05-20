import torch  # Torch is a library for deep learning
import random  # Random is a library for random number generation
import numpy as np  # Numpy is a library for numerical computation
from collections import deque  # Deque class for a fixed-size sequence
from game import SnakeGameAI, Direction, Point  # Classes from the game module
from model import Linear_QNet, QTrainer  # Classes from the model module
from helper import plot  # Plot function from the helper module

MAX_MEMORY = 100_000  # Max size of agent's memory
BATCH_SIZE = 1000  # Batch size for training the neural network
LR = 0.001  # Learning rate for training the neural network

class Agent:  # AI agent playing the Snake game

    def __init__(self):  # Initialize the Agent object
        self.num_games = 0  # Number of games played
        self.epsilon = 0  # Randomness
        self.discount_rate = 0.9  # Discount rate
        self.memory = deque(maxlen=MAX_MEMORY)    # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.discount_rate)


    def get_state(self, game):  # Get current state of the game and return it as a feature vector
        head = game.snake[0]  # Get head pos of snake
        point_l = Point(head.x - 20, head.y)  # Calc the pos to the left of head 
        point_r = Point(head.x + 20, head.y)  # Calc the pos to the right of head
        point_u = Point(head.x, head.y - 20)  # Calc the pos above the head
        point_d = Point(head.x, head.y + 20)  # Calc the pos below the head
        
        dir_l = game.direction == Direction.LEFT  # Check if snake is moving left
        dir_r = game.direction == Direction.RIGHT  # Check if snake is moving right
        dir_u = game.direction == Direction.UP  # Check if snake is moving up
        dir_d = game.direction == Direction.DOWN  # Check if snake is moving down

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # Check if the food is left of head
            game.food.x > game.head.x,  # Check if the food is right of head
            game.food.y < game.head.y,  # Check if the food is above head
            game.food.y > game.head.y  # Check if the food is below head
            ]

        return np.array(state, dtype=int)  # Convert the state to a NumPy array

    def remember(self, state, action, reward, next_state, done):  # Remember the current experience by adding it to the agent's memory
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):  # Train the neural network using a batch of experiences from the memory
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # Randomly sample a batch from the memory
        else:
            mini_sample = self.memory  # Use entire memory if size is smaller than the batch size

        states, actions, rewards, next_states, dones = zip(*mini_sample)  # Unzip the mini sample into separate lists
        self.trainer.train_step(states, actions, rewards, next_states, dones)  # Train the neural network with the mini sample
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):  # Train neural network using single experience
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):  # Get the action to take based on the current state
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.num_games  # Update epsilon value
        final_move = [0,0,0]  # Final move vector
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)  # Random move
            final_move[move] = 1  # Set corresponding action 1
        else:
            zeroRank = torch.tensor(state, dtype=torch.float)  # Convert state to a PyTorch tensor
            prediction = self.model(zeroRank)  # Get Q values predicted by the model
            move = torch.argmax(prediction).item()  # Pick action with the highest Q value
            final_move[move] = 1  # Set the corresponding action 1

        return final_move


def train():
    game_scores = []  # List to store the scores for plotting
    mean_scores = []  # List to store the mean scores for plotting
    total_score = 0  # Total score summed up across the games
    best_score = 0  # Best score achieved
    agent = Agent()  # Create an instance of the Agent class
    game = SnakeGameAI()  # Create an instance of the SnakeGameAI class
    while True:
        # Get old state
        state_old = agent.get_state(game)

        # Get move
        final_move = agent.get_action(state_old)

        # Perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Remember the experience
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Train long memory, plot result (game over)
            game.reset()  # Rest the game
            agent.num_games += 1  # Increment the # of games played
            agent.train_long_memory()

            if score > best_score:
                best_score = score
                agent.model.save()

            print('Game', agent.num_games, 'Score', score, 'best_score:', best_score)

            game_scores.append(score)  # Add the score to the game_score list
            total_score += score  # Update the total score
            mean_score = total_score / agent.num_games  # Calc mean score  
            mean_scores.append(mean_score)  # Add the mean score to the mean_score list 
            plot(game_scores, mean_scores)  # Plot scores


if __name__ == '__main__':
    train()  # Start training