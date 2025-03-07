FlipReStat - Your Personal Rocket League Stat-Tracking Discord Bot 🚀
FlipReStat is a powerful yet simple Discord bot designed to track Rocket League stats for you and your friends. Whether you're curious about your ranks, want to compare stats with others, or explore additional game modes, FlipReStat has got you covered!

🛠 Features
Meet FlipReStat, your personal Rocket League stat-tracker! Here’s what it can do:

🚀 /register: Link your Epic username to start tracking your stats.
🎮 /rank-me: View your 1v1, 2v2, and 3v3 ranks.
🔍 /rank-player: Check the ranks of any other player.
🌟 /rank-player-extra: Get ranks for extra modes like Hoops, Rumble, Dropshot, and Snowday.
📊 /stats-player: View detailed stats such as goals, assists, and saves.
📋 /player-list: See all registered players in your server.
❓ /help: Get an overview of all available commands.
📦 Installation
Follow these steps to set up FlipReStat locally:

Clone the repository:
git clone https://github.com/your-username/fliprestat.git
cd fliprestat
Install dependencies:
npm install
Set up your .env file: Create a .env file in the root directory and add the following variables:
DISCORD_TOKEN=your-discord-bot-token
USERNAME=your-username
PASSWORD=your-password
Start the bot:
node index.js
🚀 How It Works
Unfortunately, there is no free public API available for Rocket League stats. To overcome this, FlipReStat uses Cloudscraper in combination with proxies to scrape data from Rocket League Tracker Network. This ensures accurate and up-to-date stats for all players.

🖼 Screenshots (Optional)
Add screenshots or GIFs here to showcase how the bot works in action! For example:

A screenshot of the /rank-me command output.
A GIF showing the /help command.
🧰 Dependencies
FlipReStat relies on the following libraries:

Cloudscraper: For bypassing anti-bot measures while scraping data.
fake_useragent: To generate random user agents for requests.
discord.js: For building and interacting with the Discord bot.
🤝 Contributing
This is my first real project, and I’m still learning! If you’d like to contribute or improve the bot, feel free to fork the repository and submit a pull request. Here's how:

Fork the repository.
Create a new branch (git checkout -b feature/YourFeature).
Commit your changes (git commit -m 'Add YourFeature').
Push to the branch (git push origin feature/YourFeature).
Open a pull request.
🧪 Testing
If you'd like to test the bot locally, make sure you have the required environment variables set up in your .env file. Then, run the bot using:

node index.js
Test commands directly in your Discord server to ensure everything works as expected.

📜 License
This project is licensed under the MIT License. See the LICENSE file for more details.

🌟 Acknowledgments
This project wouldn’t have been possible without:

Rocket League Tracker Network for providing the data source.
The creators of the libraries used in this project.
The amazing Discord.js community for their helpful documentation and support.
💬 Contact
I’m a beginner programmer, and this is my first real project that I managed to get up and running after two weeks of trial and error. If you have any feedback, questions, or suggestions, feel free to reach out:

GitHub: @your-username
Email: your-email@example.com
Let me know if you'd like me to add anything else or refine it further! 😊