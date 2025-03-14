# HooYooTracker

HooYooTracker is a webapp that scrapes Genshin Impact and Zenless Zero codes from various sources and compiles them into one organized list. 

## Motivation

As a fan of both games and out of boredom, I decided to create a program that would simplify the process of finding released codes from these two games without having to navigate from several websites or other sources. Another reason is that I want to improve my mastery in Python as I believe I have so many things to learn, so yeah.

## Requirements

- **Windows** (Linux and macOS are also supported, but only if installed via the Docker method)
- **Python v3.10 or above**

## Installation and Usage

There are different ways to install the app. For non-techy users, installing via Releases page of this repository is recommened as you just literally click some stuff and you're good to go! However, installing the app via Docker is most recommended if you want to run the app in a Linux or macOS

### via Releases
1. Download the latest version from the [Releases](https://github.com/Scoofszlo/HooYooTracker/releases) page.
2. Extract the downloaded .zip file.
3. Open the `HooYooTracker` folder.
4. Double-click the `run.bat`.
5. Done!

### via Docker

1. Install Docker on your system
2. Build the Docker image of HooYooTracker:
    ```sh
    docker build -t hooyootracker .
    ```
3. Create a Docker volume for data storage of the app
    ```sh
    docker volume create hooyootracker_data
    ```
4. Run the Docker container:
    ```sh
    docker run -p 8080:8080 -v hooyootracker_data:/app hooyootracker
    ```
5. Open your web browser and head to `http://localhost:8080`.

### via Git clone

1. Clone the stable release:
    ```sh
    git clone -b release --single-branch https://github.com/Scoofszlo/HooYooTracker.git
    ```
2. Open the `HooYooTracker` folder.
3. Double-click the `run.bat`.
4. Done!

## Notes
- **Tested on Windows**: This program was created on Windows. The Docker version works well on my system, in which I assume that it will also work on Linux and macOS since it's the Docker that manages the stuffm though I do not guarantee that it will 100% completely  okay.
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
