# HooYooTracker

HooYooTracker is a  web application that scrapes Genshin Impact and Zenless Zero codes from various sources and compiles them into one organized list. This app can be run on Windows, macOS, or Linux.

The app is run locally and is built with TypeScript, with frameworks using React and TailwindCSS for the app interface and Cheerio, Axios, and Express.js for scraping and easy access API endpoints.

> [!IMPORTANT]  
> The old Python versions of HooYooTracker is no longer maintained and will not receive any updates. To access the old version, just switch to the `legacy` branch of this repository.

## Requirements

- Node.js (version 22.13.0 or higher)
- Windows, macOS, or Linux

## Installation

1. Install Node.js.

2. Open your terminal.

3. Clone this repository:
   ```bash
   git clone https://github.com/Scoofszlo/HooYooTracker.git
   ```

4. Run the start script:
    ```bash
    npm run start
    ```

    This script will install dependencies, build the frontend and backend, and start the servers.

5. After installation, open the HooYooTracker interface in your browser at `http://localhost:4173`.

## Usage

### General usage

To start, just run the start script in the terminal:

```bash
npm run start
```

On the very first run, it will install dependencies and build the frontend and backend, which might take a while so please be patient. On subsequent runs, it will be very fast as it will skip straight to starting the servers.

After the servers are running, you can access the app in your browser at `http://localhost:4173` to view the latest codes. If the address is not accessible, use the address shown in the terminal that has this line:

```bash
[WEB]   ➜  Local:   http://<address>:<port>/
```

To stop the app, simply press `Ctrl + C` a few times in the terminal.

### Refetching latest data

To refetch the latest codes, simply click the refresh button on the right side of the <b>"List of Codes"</b> header. This will trigger the backend to scrape the sources again and update the list with the latest codes.

> [!TIP]  
> The data will persist forever in the local storage of your browser even if you close and reopen the app again. This is to avoid unnecessary repeated scraping. However, if you wish to get the latest codes again, just simply click the refresh button again.

### Changing theme

To change the theme of the app, just click the night button on the navbar located at the upper right side of the browser interface.

## FAQs

### Will this app work offline?

Yes, it will work offline. However, you need to be connected to the internet just once to fetch the codes which will then be stored into your browser's local storage. After that, you can view the codes even when you're offline.

### Will this app work on mobile devices?

No, this app is designed to be run only in desktop running Windows, macOS, or Linux, although the design is already responsive for smaller screens.

### Will you support other games in the future?

Currently, I have no plans to support other games. However, I might consider it in the future.

### Why move from the old Python version to this new JavaScript version?

The old one actually works even until today without updates. However, I decided to not continue updating it because the code is a lot messy in there. Refactoring could take a while. Plus, I want to retain the learnings I got from building our school project that involves React + TypeScript + Node.js and wanted to learn more about some design architecturing, so I decided to build a new one from scratch using this stack. I feel like this new version is way way better and is easier to maintain.

## Contributing

If you are a developer and want to contribute to the development of HooYooTracker, you can follow these steps:

1. On the project root, install the dependencies:

   ```bash
   npm install
   ```

2. Start the development server:

    ```bash
    npm run dev
    ```

    This will start both the frontend and backend development servers with hot reloading working so that you can see your changes real-time.

3. Make your changes and test them in the browser.

4. Once you're satisfied with your changes, you can commit and push them to your forked repository.

5. Finally, create a pull request for review.

## Project versioning policy

HooYooTracker uses standard project versioning policy. Minor version is bumped for every new feature added, while patch version is bumped for bug fixes and minor changes. Major version is bumped for breaking changes.

## License

HooYooTracker is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions or concerns, feel free to contact me via the following!:
- [Gmail](mailto:scoofszlo@gmail.com) - scoofszlo@gmail.com
- Discord - @scoofszlo
- [Reddit](https://www.reddit.com/user/Scoofszlo/) - u/Scoofszlo
- [X](https://x.com/Scoofszlo) - @Scoofszlo
