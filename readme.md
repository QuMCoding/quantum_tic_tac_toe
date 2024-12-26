[繁體中文](#基於-pygame-的量子圈圈叉叉)

# Quantum Tic Tac Toe with Pygame Backend

Welcome to Quantum Tic Tac Toe! This project combines the classic game of Tic Tac Toe with the fascinating principles of quantum mechanics. The game is built using the Pygame library to provide a visually engaging and interactive experience.

## Table of Contents

1. [Installation](#installation)
2. [Game Rule](#game-rule)
3. [How to Play](#how-to-play)
4. [Requirements](#requirements)

## Installation

### Website

Click the link and play:
https://qumcoding.github.io/quantum_tic_tac_toe/

### Run on local machine

To run Quantum Tic Tac Toe on your machine, follow these steps:

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/your-username/quantum-tic-tac-toe.git
   ```

2. Navigate to the project directory:
   ```
   cd quantum-tic-tac-toe
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the game:
   ```
   python main.py
   ```

## Game Rule

This game combines the classic Tic Tac Toe with the intriguing principles of quantum mechanics. Here are the basic rules to make it easier to understand:

1. Move Rules:

    Each player takes turns placing a pair of "quantum entangled" letters in different cells, representing entanglement between those cells.
2. Superposition State:

    Before being "observed," the letters in the cells exist in an undetermined quantum superposition state.
3. Observation (collapse mode):

    When a set of "quantum entangled" cells forms a closed loop, it needs to be "observed."
    After observation, the quantum state of the letters collapses, determining the content of the cells.
    The observed symbol is sure to be "exist," and turned into a "classic" symbol, where the entanglement symbol is "vanished." When the box is observed, other symbols inside the box "vanished." When there's only one symbol left alone in the box or the symbol whose entanglement has vanished, that symbol will automatically be "classic."

    You should choose the symbol that is inside the closed loop to observe.
4. Winning Conditions:

    Once the letters are determined, the game follows the traditional Tic Tac Toe rules.
    The first player to successfully connect three letters in a row wins.
5. Tiebreaker:

    In the case of a tie where both players achieve victory conditions simultaneously, the winner is determined by comparing the maximum subscript of the connected letters, with the smaller subscript winning.

## How to play

1. Making a move

    You need to place your symbol inside the boxes, simply click the box then click the action button to place one symbol. You need to place two of these every step.

2. observation move (collapse mode)

    If a closed loop occurs, the player who's going to make the next step should choose which symbol to observe. Click the symbol you want to observe, then click the action button.

3. Winning

    Just like normal Tic-Tac-Toe, when you make a line with classic marks, you win.

## Requirements

- Python 3.5 or up
- Pygame library

# 基於 Pygame 的量子圈圈叉叉

歡迎來到量子圈圈叉叉！該專案將經典的圈圈叉叉與迷人的量子力學原理互相結合，使用 Pygame 構建，提供視覺上的精采體驗。

## 目錄

1. [安裝](#安裝)
2. [遊戲規則](#遊戲規則)
3. [如何遊玩](#如何遊玩)
4. [環境](#環境)

## 安裝

### 網頁

點擊以下連結並遊玩：
https://qumcoding.github.io/quantum_tic_tac_toe/

### 在本機電腦運行

依照以下步驟以在本機電腦上運行量子圈圈叉叉：

1. 複製此儲存庫到你的電腦：
    ```
    git clone https://github.com/your-username/quantum-tic-tac-toe.git
    ```

2. 切換至專案目錄：
    ```
    cd quantum-tic-tac-toe
    ```

3. 安裝依賴：
    ```
    pip install -r requirements.txt
    ```

4. 運行遊戲：
    ```
    python main.py
    ```

## 遊戲規則

本遊戲將經典的圈圈叉叉與迷人的量子力學原理互相結合。以下是幾個讓此遊戲更容易理解的幾個規則：

1. 移動規則：
    每個玩家輪流在兩個不同的格子中放置一對「量子糾纏」字母（O 或 X），代表這兩格之間的糾纏關係。

2. 疊加態：
    在被「觀測」之前，格子中的字母以不確定的量子疊加態存在。

3. 觀測（坍縮模式）
    當一組「量子糾纏」的格子形成一個封閉迴圈時，就需要對其進行「觀測」。
    觀察後，字母的量子態坍縮，決定了格子中的字母。
    觀察的字母必定「存在」，並變成了「確定的」字母。當盒子被確定後，盒子內的其他字母就「消失」了。當盒子裡只剩下一個符號或糾纏消失的符號時，符號也是「確定的」。

4. 勝利條件
    一旦確定了字母，遊戲就遵循傳統的圈圈叉叉遊戲規則：第一個成功三個字母連成一線的玩家獲勝。

5. 決勝局
    如果雙方同時達到勝利條件且平局，則透過比較相連字母中最大下標來確定獲勝者，較小的下標獲勝。

## 如何遊玩

1. 下棋
    您需要將字母放置在框中，只需按一下該格子，然後按一下 `action` 按鈕即可放置一個字母。每一步都需要放置兩個。

2. 觀測（坍縮模式）
    如果發生封閉迴圈，要進行下一步的玩家應該選擇觀察哪個字母。按一下您要觀察的字母，然後按一下 `action` 按鈕。

3. 勝利
    就跟普通的圈圈叉叉一樣，只要連成一線即獲勝。

## 環境

* Python 3.5 (含)以上
* Pygame
