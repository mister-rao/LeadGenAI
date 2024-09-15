# LeadGenAI

LeadGenAI is a workflow to generate and optimize personalized lead generation emails using two Large Language Models (LLMs), orchestrating the content for maximum effectiveness. It leverages **LangGraph** to model agents and tools.

## Features

- **Dual-Language Model Workflow**: Uses two different OpenAI models (gpt-4 and gpt-3.5-turbo) LLMs to generate personalized emails.
- **Quality Checking**: Uses gpt-4o to compare the two generated emails and select the best one. 
- **Orchestration with LangGraph**: agents and tools are modelled using LangGraph (gpt-3.5-turbo).
- **Interactive Notebooks**: All project components are contained within Jupyter Notebooks for ease of use and experimentation.

## Installation

LeadGenAI uses [Poetry](https://python-poetry.org/) for dependency management. Follow the instructions below to set up your environment.

### Prerequisites

- Python 3.12
- Poetry (If not installed, you can find the installation instructions [here](https://python-poetry.org/docs/#installation))

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/mister-rao/LeadGenAI.git
    cd LeadGenAI
    ```

2. Install the dependencies using Poetry:
    ```bash
    poetry install
    ```

3. Activate the virtual environment:
    ```bash
    poetry shell
    ```

4. Launch Jupyter Notebook:
    ```bash
    jupyter lab
    ```

## Usage

Once the environment is set up, you can open the provided Jupyter notebook to start generating personalized lead emails using the integrated LLMs.


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph) for orchestration support.
- [OpenAI](https://openai.com/) for providing powerful models for content generation.
