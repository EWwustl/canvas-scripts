# Canvas scripts to gather quiz responses & students mapping from Canvas

Author: Yuchen (Eric) Wei

Inspired by professor Bill Siever's canvas scripts

# Table of content:

-   [Setup Instructions](#setup-instructions)

-   [Usage](#usage)

<a id="setup-instructions"></a>

## Setup Instructions

### Prerequisites

Before setting up, ensure you have Miniconda installed on your computer. Conda is an open source environment and package manager. Miniconda is a free installer for Conda, Python, and a few other useful packages.

### Step 1: Install Miniconda

1. Download Miniconda:

    - Go to the [Miniconda installation page](https://docs.anaconda.com/free/miniconda/miniconda-install/).
    - Download the appropriate installer for your operating system (Windows, macOS, or Linux).

2. Install Miniconda:

    - Follow the instructions on the installation page.

    - For Windows system, during installation, ensure the option to add Miniconda to your PATH environment variable is checked.

3. Restart your computer after the installation finishes.

### Step 2: Set Up the Virtual Environment

-   **Windows**: Double click to execute `setup.bat` to automatically set up the virtual environment

-   **MaxOS / Linux**:

    1. [Open this folder in terminal](https://support.apple.com/en-in/guide/terminal/trmlb20c7888/mac)
    2. Execute `make_executable.sh` by running `./make_executable.sh` in terminal
    3. Close the terminal
    4. Double click to execute `setup.sh` to automatically set up the virtual environment

-   Ignore the 'pip dependency' error if it occurs during setup as it does not affect the execution of our scripts

### Step 4: Setup `CanvasSettings.py`

1. Copy the `CanvasSettingsTemplate.py` file

2. Rename the copy as `CanvasSettings.py`

3. Set the variables in `CanvasSettings.py` according to instructions in the comments

### Step 5: Check Quizzes in Canvas

-   Make sure each question in your quizzes has a short, descriptive name (e.g. 'time spent'), this is necessary for the output CSV files to have correct fieldnames

-   **This only supports Multiple Choice Questions and Essay Questions in Quizzes**

<a id="usage"></a>

## Usage:

-   To automatically fetch the quiz responses & students mapping and output them into CSV files:

    -   **Windows**: Double click to execute `run.bat`
    -   **MacOS / Linux**: Double click to execute `run.sh`

-   If there's ever a need to re-process a specific quiz, just delete the CSV file for that quiz and re-execute the run file
