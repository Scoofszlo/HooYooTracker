# HooYooTracker

HooYooTracker is a webapp that scrapes Genshin Impact and Zenless Zero codes from various sources and compiles them into one organized list. 

## Motivation

As a fan of both games and out of boredom, I decided to create a program that would simplify the process of finding released codes from these two games without having to navigate from several websites or other sources. Another reason is that I want to improve my mastery in Python as I believe I have so many things to learn, so yeah.

## Requirements

- **Windows, Linux or macOS**
- **Python v3.10 or above**

## Installation

### via GitHub Releases/Git clone (supports Windows/Linux)
1. Get the latest release by either of the following methods:
    - Download the latest version from the [GitHub Releases](https://github.com/Scoofszlo/HooYooTracker/releases) page.
    - Clone the stable release using Git:
        ```sh
        git clone -b release --single-branch https://github.com/Scoofszlo/HooYooTracker.git
        ```
2. Extract the downloaded .zip file (if downloaded via GitHub Releases).
3. Open the `HooYooTracker` folder.
4. Double-click the `run.bat` for Windows or `run.sh` for Linux. (For Linux users, ensure `Allow executing file as program` checkbox is checked to be able to run it.)
5. Done!

### via Docker (supports Windows/Linux/macOS)

1. Install Docker on your system.
2. Build the Docker image of HooYooTracker:
    ```sh
    docker build -t hooyootracker .
    ```
3. Create a Docker volume for data storage of the app:
    ```sh
    docker volume create hooyootracker_data
    ```
4. Run the Docker container:
    ```sh
    docker run -p 8080:8080 -v hooyootracker_data:/app hooyootracker
    ```
5. Open your web browser and head to `http://localhost:8080`.
6. Done!

## Usage

Once installed, simply click `run.bat` or `run.sh` (depending on your operating system) to run the app. For Docker users, you can run the command to start the program or start it via the Docker app.

On first startup, wait for the app to get the data from sources for Genshin Impact. Once finished, it will display the list of codes as well as their reward details. You can click on the code, which will redirect you to the official redeem website with the code already in the text field.

You can click `Refresh data` to get the latest updates anytime. To switch games, simply click the game name of your choice.

To close the program, simply stop the terminal. For Docker users, you can also stop it in the terminal or via their app.

## Notes
- **Limited testing was done**: The project development is mainly done on Windows. As of March 18, 2025, the app now supports Linux and macOS. However, limited testing was done for these operating systems so I do not guarantee that this will work for everyone (so please raise an issue if something goes wrong!)
- **Currently supports Python v3.10 and up**: This program was supposed to support at least Python v3.8 but due to certain features that I have used throughout the program and external dependencies requirement, only Python v3.10 and above are only supported.

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature/YourFeature
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```sh
    git push origin feature/YourFeature
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or concerns, feel free to contact me via the following!:
- [Gmail](mailto:scoofszlo@gmail.com) - scoofszlo@gmail.com
- Discord - @scoofszlo
- [Reddit](https://www.reddit.com/user/Scoofszlo/) - u/Scoofszlo
- [Twitter](https://twitter.com/Scoofszlo) - @Scoofszlo
