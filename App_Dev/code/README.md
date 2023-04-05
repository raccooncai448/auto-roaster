# Auto-Roaster

<h3 align="center"> Friend or foe? Yay or no? Send a compliment over to tip your hat, or generate a sly roast for a laugh. All generated and automated by the latest advances in deep learning for vision-language! </h3>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

In a virtual environment, use pip to download the following libraries.
* pip
  ```sh
  pip install replicate opencv-python
  pip install --upgrade openai
  ```

### Installation
(*Note: We have already provided an API Key for Replicate, but you need an OpenAI account with credits to get the OpenAI token.*)
1. Get a free Replicate API Key at [https://replicate.com/account](https://replicate.com/account).
2. In shell, set the token as an environment variable.
   ```sh
   export REPLICATE_API_TOKEN=[token]
   ```
   For windows, use command
   ```sh
   set REPLICATE_API_TOKEN=[token]
   ```
3. Get a free OpenAI Key.
  ```sh
  export OPENAI_API_KEY=[key]
  ```
5. Clone the repo
   ```sh
   git clone https://github.com/jjchilling/Auto-Roaster
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
### main.py
1. In shell, run
  ```sh
  python main.py
  ```
2. The script will ask if you want a roast or compliment (type in 'roast' or 'compliment' exactly without the quotes)
3. Allow webcam access if requested.
4. After taking the photo, click any key to continue.
5. Enjoy your AI-generated comment (takes around 10 seconds on CPU)! Comments are cached in the cachedComments file, and images are saved in the demo file.

### preloaded.py
1. Save an image to the demo folder (.png, .jpeg, .jpg supported)
2. In shell, run
  ```sh
  python preloaded.py
  ```
3. The script will ask if you want a roast or compliment (type in 'roast' or 'compliment' exactly without the quotes)
4. The script will ask for the subject (type in either 'dog.jpeg', 'cat.jpeg', or 'cpax.jpeg' for sample images, or your image file name)
5. Enjoy your AI-generated comment (takes around 10 seconds on CPU)! Comments are cached in the cachedComments file, and images are saved in the demo file.

*For samples, please refer to the demo folder.*

<p align="right">(<a href="#readme-top">back to top</a>)</p>
