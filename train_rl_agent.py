import os
import gym
import numpy as np
import pandas as pd
from stable_baselines3 import DQN
from gym import spaces

DATA_DIR = 'data'
TICKER = 'AAPL'  # Change to desired ticker
CSV_PATH = os.path.join(DATA_DIR, f'{TICKER}_intraday.csv')

class TradingEnv(gym.Env):
    def __init__(self, df):
        super().__init__()
        self.df = df.reset_index(drop=True)
        self.current_step = 0
        self.balance = 10000  # Starting cash
        self.shares_held = 0
        self.action_space = spaces.Discrete(3)  # 0: Hold, 1: Buy, 2: Sell
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        self.balance = 10000
        self.shares_held = 0
        return self._get_obs()

    def _get_obs(self):
        row = self.df.iloc[self.current_step]
        return np.array([
            row['1. open'], row['2. high'], row['3. low'], row['4. close'], self.balance
        ], dtype=np.float32)

    def step(self, action):
        row = self.df.iloc[self.current_step]
        price = row['4. close']
        reward = 0
        # Buy
        if action == 1 and self.balance >= price:
            self.shares_held += 1
            self.balance -= price
        # Sell
        elif action == 2 and self.shares_held > 0:
            self.shares_held -= 1
            self.balance += price
            reward = price  # Reward: profit from sale
        self.current_step += 1
        done = self.current_step >= len(self.df) - 1
        obs = self._get_obs() if not done else np.zeros(self.observation_space.shape)
        return obs, reward, done, {}

if __name__ == '__main__':
    df = pd.read_csv(CSV_PATH)
    env = TradingEnv(df)
    model = DQN('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=10000)
    model.save('dqn_trading_agent')
    print('Training complete. Model saved as dqn_trading_agent.')
