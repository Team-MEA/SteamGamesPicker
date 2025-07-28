# 🎮 Steam Games Picker

**Navigate Your Vast Game Library with Ease!**

The Steam Games Picker is a powerful backend system designed to help you (and your friends!) effortlessly narrow down a massive collection of games to find that perfect next pick. Tired of endless scrolling and indecision? This application intelligently filters, sorts, and presents games in manageable batches, keeping track of your journey every step of the way.

--------------
![Setup Sample](/assets/StartUpMenu.png "Setup Sample")

![Display Sample](/assets/GameDisplayMenu.png "Display Sample")
--------------
## Why?

## 📱 Features:

*   **Intelligent Batch Generation**: Dynamically creates batches of games, reducing the number of choices as you progress.
*   **Interactive Filtering**:
    *   **Finds common games** shared with selected friends.
    *   **Hard filters** by multiple tags, ensuring games possess *all* specified genres or characteristics.
    *   **Filters by playtime**, helping you discover quick sessions or epic sagas.
*   **Comprehensive Tag Extraction**: Automatically gathers all unique tags from your game library for easy filtering options.
*   **Robust State Management (Undo/Redo)**: Never fear a wrong decision! The app maintains a full history of your filtering process, allowing you to freely undo and redo steps until you find your ideal game.
*   **Final Pick Identification**: Clearly identifies the single chosen game once the selection process is complete.
*   **Modular & Tested Design**: Built with robust validation and unit-tested components, ensuring reliability and maintainability.

## 🧩 How It Works (Core Logic):

The system leverages a sophisticated `Session` manager that orchestrates `State` objects, each representing a unique snapshot of your game selection journey. Games are intelligently moved between `"remaining,"` `"batch,"` and `"seen"` pools, driven by your confirmations and filtering choices. Core utilities handle complex operations like set intersections for common games and and precise tag-based filtering.

## 🔧 Installation

To set up and run the Steam Games Picker's core logic, follow these steps:

### Prerequisites

*   Python 3\.8 or higher installed on your system\.
*   \`tkinter\` library installed (usually included with Python\, but may require a separate system package like \`python3\-tk\` on some Linux distributions)\.

### Step 1: Clone the Repository

First, clone the project repository from GitHub to your local machine\:

```bash
git clone https://github.com/Team-MEA/SteamGamesPicker.git
cd SteamGamesPicker
```

### Step 2: Create a Virtual Environment

It's highly recommended to create a Python [virtual environment](https://docs.python.org/3/library/venv.html). This isolates your project's dependencies from your system-wide Python installation, preventing conflicts.

```bash
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment

Activate the virtual environment\. The command depends on your operating system\:

*   **On Linux/macOS**:
    ```bash
    source venv/bin/activate
    ```
*   **On Windows (Command Prompt)**:
    ```cmd
    venv\Scripts\activate.bat
    ```
*   **On Windows (PowerShell)**:
    ```powershell
    venv\Scripts\Activate.ps1
    ```

You should see `(venv)` prepended to your terminal prompt\, indicating the virtual environment is active\.

### Step 4: Install Dependencies

You can install part of them using `pip`:

```bash
pip install -r requirements.txt
```

chrome and chromedriver are also needed.


## Installation guide for chrome and chromedriver dependancies:

# Ubuntu/WSL:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
google-chrome --version
```
```bash
wget https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.168/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
chromedriver --version
```
google-chrome and chromedriver need to have the same version, so modify the version part of the command accordingly.

# Windows:
 1. Download Google Chrome from https://www.google.com/chrome/
 2. Open Chrome and go to chrome://settings/help to find version
 3. Download the matching ChromeDriver from https://sites.google.com/chromium.org/driver/
 4. Unzip chromedriver.exe and place in a folder in your PATH
 5. In Command Prompt or PowerShell, check:
```bash
chromedriver --version
```
# MacOS:
 Download Chrome from https://www.google.com/chrome/
 Download ChromeDriver from https://sites.google.com/chromium.org/driver/
 ```bash
unzip chromedriver-mac-x64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
chromedriver --version
```

### Step 5: Run the Application

**To run the main application**:

Make sure your virtual environment is active (Step 3). From the project's root directory (`SteamGamesPicker/`),, execute:

```bash
python3 main.py
# or
python main.py
```

## State of the project:
The project is in its MVP state and will be improved upon.

## Contributors
Massive shout out to our contributors for this Hackathon. This project wouldnt have been feasible without that.
This project was incredibly fun and stressfull, thank you for all your work.

- [@EluxRed](https://github.com/EluxRed)
- [@5PenguinsInATrenchCoat](https://github.com/5PenguinsInATrenchCoat)
- [@Awowz](https://github.com/Awowz)
