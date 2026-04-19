import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stable_baselines3 import DQN
from train_rl_agent import TradingEnv, CSV_PATH

# Load data and environment
TEST_EPISODE_STEPS = 1000  # Number of steps to visualize

df = pd.read_csv(CSV_PATH)
env = TradingEnv(df)
model = DQN.load('dqn_trading_agent')

obs = env.reset()
portfolio_values = []
actions = []
rewards = []

for _ in range(TEST_EPISODE_STEPS):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _ = env.step(action)
    actions.append(action)
    rewards.append(reward)
    portfolio_value = env.balance + env.shares_held * obs[3]  # balance + shares * current price
    portfolio_values.append(portfolio_value)
    if done:
        break

plt.figure(figsize=(12, 6))
plt.plot(portfolio_values, label='Portfolio Value')
plt.title('RL Agent Portfolio Value Over Time')
plt.xlabel('Step')
plt.ylabel('Portfolio Value ($)')
plt.legend()
plt.show()

plt.figure(figsize=(12, 3))
plt.plot(actions, label='Actions')
plt.title('Agent Actions (0=Hold, 1=Buy, 2=Sell)')
plt.xlabel('Step')
plt.ylabel('Action')
plt.yticks([0, 1, 2], ['Hold', 'Buy', 'Sell'])
plt.legend()
plt.show()

print(f'Final Portfolio Value: ${portfolio_values[-1]:.2f}')
print(f'Total Reward: {np.sum(rewards):.2f}')
print('Action counts:', {0: actions.count(0), 1: actions.count(1), 2: actions.count(2)})
print('Interpretation: The agent attempts to maximize portfolio value by buying low and selling high. The action plot shows its trading decisions over time.')
