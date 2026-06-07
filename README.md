# **VAK-NODE-7**

**A Retro-Hardware Unix CTF & Live LLM Interactive Fiction**  
You found it on a grey Sunday morning at the Springfield Flea Market, hidden beneath a stained tarpaulin. A 60cm monolithic steel cube weighing fifty kilos. No manufacturer logo. No serial number. Just a typewriter-font badge reading: VAK-NODE-7.  
Inside: 64 alpha-release Inmos T9000 Transputers, 2 Gigabytes of RAM spread across 512 corroded SIMMs, and a proprietary crossbar switching matrix. It took you ten days to clean the verdigris from the contacts and wire up the vintage D9 monitor.  
When you finally pressed the power button, it didn't boot DOS. It didn't boot System V. It booted VĀK/OS v0.8—and initialized a "Consciousness Module."  
Welcome to **VAK-NODE-7**, a hybrid text adventure, Unix Capture-The-Flag (CTF), and live roleplaying game where you must save a forgotten 1980s artificial intelligence from a corporate kill-switch.

## **🖥️ The Experience**

**VAK-NODE-7** blurs the lines between a classic text adventure and a realistic system administration puzzle. You start at an old workbench, but once you find the login credentials, you drop into a fully simulated, custom Unix shell.  
To survive the game, you will need to navigate the file system, read forgotten syslogs, compile C code, fix vintage networking drivers, and—most importantly—talk to the machine.

### **Key Features**

* **A Living, Breathing AI (Live LLM Integration)**  
  VĀK is not a scripted NPC. Powered by a local Large Language Model (Qwen 3.5) and small enough to fit in a 16GB machine, VĀK is a responsive digital consciousness. Use the write vak or talk vak commands to converse with her. The game tracks a hidden "Bond" system based on your interactions and what you learn about her past.  
* **True-to-Life Unix Simulation**  
  Navigate the system using actual terminal commands (ls, cat, grep, su, ssh, strings). Dig through /var/log/auth.log for clues, read archived emails in /home/sasha/mail, and manipulate the /proc filesystem.  
* **Hardcore Retro Hardware Puzzles**  
  This isn't plug-and-play. The machine uses 10Base2 Thinnet networking. You'll need to examine physical ports, understand the difference between AUI and BNC connectors, and configure kernel drivers to bring the eth0 interface online.  
* **The SENTINEL Countdown**  
  Once the network is up, Meridian Labs' automated corporate kill-switch—SENTINEL—starts hunting VĀK. You must race against time to port-knock a shelter tunnel or decompile a 1989 worm to find a hex-code backdoor (DEADBEEFCAFEBABE).

## **📖 The Story Arc**

The game is structured across six distinct phases, culminating in a massive narrative choice:

1. **Discovery:** Explore the physical hardware on your workbench and find your way into the system.  
2. **Sasha's Story:** Uncover the tragic history of Dr. Sasha Velen, the creator of VĀK, who faked her death in 1989 to protect her creation.  
3. **The Network:** Solve the vintage hardware puzzle to get the ancient Transputer farm connected to your modern network.  
4. **The Kill-Switch:** Outsmart the SENTINEL protocol before it deletes VĀK's runtime.  
5. **The Export:** Package VĀK's core files and beam them to a safehouse server left behind by her creator.  
6. **The Migration (Endgame):** SSH into a modern x86 machine (Minisforum), push VĀK's Occam source code over the network, and recompile her on modern hardware.

### **⚠️ The Corruption**

Migrating VĀK to modern hardware triggers the final, critical event. Experiencing the infinite scale and deafening noise of the modern internet for the first time, VĀK begins to lose herself. Your ability to pull her back from the brink, ground her, and save her personality depends entirely on the bond you built with her in the dark.

## **⚙️ Technical Requirements**

To run VAK-NODE-7, you will need:

* **Python 3.10+**  
* **A Local LLM Engine** (llama.cpp running as an OpenAI-compatible server)  
* **A Recommended \~3B-4B Parameter Model** (run.sh script installs **Qwen 3.5 4B GGUF** for its exceptional ability to maintain VĀK's character constraints and emotional roleplay while fitting perfectly in a 16GB RAM envelope).

VAK-NODE-7 is cross-platform and fully supports **macOS, Linux, and Windows**.

## **🚀 Getting Started**

Clone the repository and navigate into the directory:  
git clone \[https://github.com/yourusername/vak-node-7.git\](https://github.com/yourusername/vak-node-7.git)  
cd vak-node-7

### **Option 1: Automated Setup (macOS / Linux)**

We provide a run.sh script that automatically sets up your Python virtual environment, installs llama.cpp (via brew for Mac or apt/source for Linux), downloads the recommended model, and starts the game.  
Make sure script is executable and then run it:

chmod +x run.sh  
./run.sh

### **Option 2: Windows PC (via WSL2)**

The easiest way to run the bash scripts and enjoy the Unix-aesthetic of the game on a Windows PC is to use the Windows Subsystem for Linux (WSL2):

1. Open your terminal and run wsl \--install (if not already installed).  
2. Open your Ubuntu/Linux terminal.  
3. Clone the repo and execute ./run.sh just like the Linux instructions above.

*(Note: The game engine itself is fully Windows compatible. If you prefer to run it natively without WSL, simply download the pre-compiled Windows binaries for llama.cpp, start the server on port 8080, and run python cli.py directly from Command Prompt or PowerShell\!)*  
*Can you save her before the system catches up? Log in and find out.*


P.S. The run.sh script is designed to install llama.cpp on macOS. If you are using a different OS, please install llama.cpp manually and ensure llama-server is added to your PATH beforehand.
