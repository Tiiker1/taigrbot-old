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
- clear command<br>
- poll command<br>
- reporting bug and message context menu commands<br>
- github commit output to specified channel<br>
- welcome and leave messages which need to be configured in main code<br>

## Changelog:
( - means added and x means removed )<br>
<h4>06.05.2024</h4>
- added leave and welcome messages for configured guild and channels<br>
x removed report bug and message commands from main code since they now exists on commands folder in seperated files.<br>
<h4>30.04.2024</h4>
- better readme file<br>
x removed poll command since its replaced by more advanced poll command<br>
- Enhanced poll command<br>
<h4>29.04.2024</h4>
- context menu commands (report bugs and report message to moderators)
<h4>soon after intial commit</h4>
- clear command

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
- [ ] fix clear commmand to show amount messages it actually deleted not what you told it to delete
- [ ] Github script to own scripts folder
- [ ] Add more feature
- [x] Changelog 01.05.2024
- [x] Poll command 30.04.2024


<!-- LICENSE -->
## License

Software provided does not come with any kind of warranty and im not resposible any possible damage it has caused or could cause.<br>
You use this software completly under your own responsibility.<br>
You are not allowed to freely use this provided software.<br>
For now you can use it in your projects long as you keep it open source or fork it directly on github.<br>
organisations and corporates and official use of this bot is not allowed. (for a fee i´ll give permissions to directly use this bot for those mentioned before.) 



<!-- CONTACT -->
## Contact

Email -  tkr1.cloud@gmail.com

Project Link: [https://github.com/Tiiker1/taigrfull](https://github.com/Tiiker1/taigrfull)


<!-- ACKNOWLEDGMENTS -->
## Resources

I found these recoures usefull when i started this project

* [Choose an Open Source License](https://choosealicense.com)
* [Discord.py docs](https://discordpy.readthedocs.io/en/stable/)
