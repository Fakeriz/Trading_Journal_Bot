# Trading Journal Bot

This repository contains a **Trading Journal Bot** designed to help traders manage and track their trades efficiently. The bot offers a variety of features to streamline the process of logging, reviewing, and exporting trade data, making it an essential tool for traders who want to maintain a detailed and organized trading journal.

## Features

- **Export to CSV:** Easily export your trading data to a CSV file for offline analysis or record-keeping.
- **Advanced Search Options:** Search your trades by ticker, side (buy/sell), and status within specific periods like 1 week, 1 month, 3 months, etc.
- **Inline Keyboard Buttons:** Intuitive InlineKeyboardButton interface for selecting specific months and navigating through different periods.
- **Date/Time Validation:** Ensure accurate logging of trades with built-in date and time validation.
- **Period-Based Trade Review:** The bot can prompt users to review their trades within a specified date range, making it easier to track performance over time.
- **Comprehensive Documentation:** The codebase is thoroughly documented with comments and docstrings to help users understand the functionality and facilitate future development.

## Getting Started

### Prerequisites

To run this bot, you will need:

- Python 3.x installed on your machine.
- Required Python libraries as specified in `requirements.txt`.

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Fakeriz/Trading_Journal_Bot.git
    cd Trading_Journal_Bot
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the bot:
    ```bash
    python bot.py
    ```

## Usage

Once the bot is running, you can interact with it to log new trades, search for past trades based on various filters, and export your trade history to a CSV file. The bot is designed with user-friendly navigation and validation checks to ensure a smooth experience.



## How to Create a New Bot and Add the Token to Your Project

To get your Trading Journal Bot up and running, you need to create a new bot on Telegram using BotFather and configure it in your project. Follow these steps:

### Step 1: Create a New Bot Using BotFather

1. **Open Telegram** and search for **BotFather** (the official bot for managing all Telegram bots).
2. **Start a chat** with BotFather by clicking on the `/start` button or typing `/start`.
3. To create a new bot, type the command `/newbot`.
4. **Name your bot** when prompted. This will be the display name of your bot.
5. **Choose a username** for your bot. The username must be unique and end with `bot` (e.g., `MyTradingJournalBot`).
6. After successful creation, BotFather will provide you with a **Bot Token**.

### Step 2: Add the Bot Token to Your Project

1. **Copy the Bot Token** provided by BotFather. This token is essential for authenticating your bot with the Telegram API.

2. **Create a `.env` file** in the root directory of your project (if it doesn’t already exist).

3. Add the following line to your `.env` file, replacing `YOUR_BOT_TOKEN` with the actual token you received from BotFather:
    ```env
    TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
    ```

    Example:
    ```env
    TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjkLmNOPQrstUVwxyZ1234567
    ```

### Step 3: Run Your Bot

1. With the `.env` file set up, your bot is ready to run. You can start your bot using the following command:
    ```bash
    python main.py
    ```

2. Your bot should now be connected to Telegram and ready to interact with users!


## Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please feel free to reach out via GitHub or open an issue in this repository.

