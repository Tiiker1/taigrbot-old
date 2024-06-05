<div align="center">
  <h3 align="center">taigrfull</h3>
  <p align="center">
    full dev version of taigrbot which has all features.
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Features">Features</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## Features

Current features of this bot:<br>
- utility comands<br>
- moderation commands (under commands/moderation)<br>
- other commands (not defined yet)
- reporting bug and message context menu commands<br>
- github commit output to specified channel<br>
- welcome and leave messages which need to be configured in main code<br>

## Changelog:

<h4>05.06.2024</h4>
- modified buttons command with following changes:<br>
- rename for rolemenu command in file and usage<br>
- rename for add_option to addrole<br>
- rename for remove_option to removerole<br>
- 
- started developing frontend to be more clear and more usable for end users

<h4>04.06.2024</h4>
- added xp system with leaderboard and xp command<br>
- added xp system imports and setupcall functions<br>
- modified MyClient class to work with xpsystem<br>
- modified on_message event to work with xpsystem<br>
- made so that xp system uses database in databases folder which has per guild information<br>
- modified help command to have new commands and better looking<br>

<h4>27.05.2024</h4>
- relocated json files to jsondata and it will store data there from various commands now<br>
- modified report_contextmenu command so it stores its data to json file and has now also feature to set reported messages channel per guild<br>
  with command /setlogchannel channel_name_here<br>
- modified codes so that instead of commit_data folder all json files go to jsondata folder<br>

<h4>22.05.2024</h4>
- added visitturku command<br>
- added visitturku imports and call setup functions<br>
- fixed visitturku command so it no longer send empty article at first and stores data littlebit better<br>

<h4>18.05.2024</h4>
- added review command (reguries reviews channel to work)<br>
- added imports for review command<br>
- added features folder insider commands folder<br>

<h4>15.05.2024</h4>
- modified and fixed imports for help ahelp and buttons command<br>
- added ahelp (ahelp is help command for adminstrative commands)<br>
- added customizable rolemenu feature and commands for it<br>
- relocated help command to information folder<br>
- created inforamtion folder for information commands<br>

<h4>13.05.2024</h4>
- modified imports of moderation commands to them begin able to be in sub folder<br>
- created moderation folder to commands for better manage of commands<br>
- relocated moderation commands to moderation subfolder<br>
- added custom status for bot (not yet commited)

<h4>08.05.2024</h4>
- added imports and setup call functions for mute, unmute and help commands<br>
- added mute and unmute commands to help command<br>
- added task to check every 10minutes for new commits<br>
- added seperate github.py script to scripts folder to send messages about github commits automaticly on dev channel<br>
- removed github script from main file<br>

<h4>07.05.2024</h4>
- added mute command<br>
- added unmute command<br>
- added help command<br>

<h4>06.05.2024</h4>
- added leave and welcome messages for configured guild and channels<br>
x removed report bug and message commands from main code since they now exists on commands folder in seperated files.<br>

<h4>30.04.2024</h4>
- better readme file<br>
- removed poll command since its replaced by more advanced poll command<br>
- added Enhanced poll command<br>

<h4>29.04.2024</h4>
- added context menu commands (report bugs and report message to moderators)
<h4>soon after intial commit</h4>
- added clear command

## Built With

Python libraries/modules used in this project

* discord.py
* discord.ext
* typing
* requests
* os
* datetime
* pytz
* json
* yarl


<!-- GETTING STARTED -->
## Getting Started

Follow these instructions if you want to run this bot

### Prerequisites
These are required to install before getting started:<br>
Python from: https://www.python.org/downloads/

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Tiiker1/taigrfull.git
   ```
2. Install pip packages
   ```sh
   pip install -r requirements.txt
   ```
3. Enter your discord bot token in `bot.py`
   ```
   client.run("enter your token here")
   ```
4. Run the bot in terminal with this command
   ```sh
   python bot.py
   ```


<!-- USAGE EXAMPLES -->
## Usage

to start this bot open command promopt in same folder as bot is and do following command:
   ```sh
   python bot.py
   ```

<!-- ROADMAP -->
## Things to do which was not originally on this bot

- [ ] Event files to own folder
- [ ] production ready version
- [x] Github script to own scripts folder 08.05.2024
- [x] Changelog 01.05.2024

<!-- LICENSE -->
## License

Software provided does not come with any kind of warranty and im not resposible any possible damage it has caused or could cause.<br>
You use this software completly under your own responsibility.<br>
If you want to host your own version on this please do fork!<br>
If you use this code you are required to keep your project open source.<br>
any changes to license will apply to older versions and current and new versions.<br>
this license needs to applied also on forks or own versions of this bot and it will need to updated if this license is updated.<br>
downloading or using this code you agree this license and will follow it.<br>

<!-- CONTACT -->
## Contact

Email -  tkr1.cloud@gmail.com

Project Link: [https://github.com/Tiiker1/taigrfull](https://github.com/Tiiker1/taigrfull)


<!-- ACKNOWLEDGMENTS -->
## Resources

I found these recoures usefull when i started this project

* [Choose an Open Source License](https://choosealicense.com)
* [Discord.py docs](https://discordpy.readthedocs.io/en/stable/)
* [information about buttons](https://gist.github.com/lykn/bac99b06d45ff8eed34c2220d86b6bf4)
  
