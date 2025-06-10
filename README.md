# AiNewsCrew Crew

Welcome to the AiNewsCrew Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/ai_news_crew/config/agents.yaml` to define your agents
- Modify `src/ai_news_crew/config/tasks.yaml` to define your tasks
- Modify `src/ai_news_crew/crew.py` to add your own logic, tools and specific args
- Modify `src/ai_news_crew/main.py` to add custom inputs for your agents and tasks

## Running the Project

### Option 1: Streamlit Web Interface (Recommended)

Launch the interactive web interface for a user-friendly experience:

```bash
uv run streamlit run streamlit_app.py
```

This will start a local web server (typically at `http://localhost:8501`) where you can:
- Enter any research topic in the web interface
- Click "Start Research" to begin the AI crew's work
- View the generated report directly in your browser
- No files are created - all output is displayed in the web interface

### Option 2: Command Line Interface

To run the crew from the command line with a predefined topic:

```bash
$ crewai run
```

This command initializes the ai-news-crew Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The ai-news-crew Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## OpenLIT Observability (Optional)

This project includes optional OpenLIT integration for comprehensive AI observability, allowing you to monitor agent interactions, task execution metrics, and system performance.

### Prerequisites

- Docker Desktop installed and running
- At least 2GB of available RAM for OpenLIT services
- Ports 3001, 4317, 4318, 8123, 8888, 9000, and 55679 available

### Starting OpenLIT Services

To enable observability monitoring:

```bash
# Start OpenLIT services in the background
docker compose up -d

# Verify services are running
docker compose ps
```

The following services will be available:
- **OpenLIT Dashboard**: http://localhost:3001 - Main observability interface
- **ClickHouse**: localhost:8123 - Database for telemetry data
- **OpenTelemetry Collector**: localhost:4318 - Receives telemetry data
- **Collector Metrics**: http://localhost:8888/metrics - Prometheus metrics
- **ZPages**: http://localhost:55679 - Collector debugging interface

### Using with Observability

When OpenLIT services are running, the Streamlit application will automatically send telemetry data to the collector. You can monitor:

- Agent execution traces
- Task completion metrics
- Performance statistics
- Error rates and debugging information

### Stopping OpenLIT Services

```bash
# Stop and remove containers
docker compose down

# Stop and remove containers with volumes (clears all data)
docker compose down -v
```

### Troubleshooting

**Services won't start:**
- Ensure Docker Desktop is running
- Check that required ports are not in use: `lsof -i :3001,4317,4318,8123,9000`
- Verify available system resources

**No data in dashboard:**
- Confirm OpenTelemetry Collector is receiving data at http://localhost:55679
- Check collector logs: `docker compose logs otel-collector`
- Ensure the Streamlit app is running with OpenLIT integration enabled

**Performance issues:**
- Resource limits are configured for local development
- Adjust memory limits in `docker-compose.yml` if needed
- Monitor resource usage: `docker stats`

## Support

For support, questions, or feedback regarding the AiNewsCrew Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
