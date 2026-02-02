from agent_builder import AgentBuilder

def main():
    builder = AgentBuilder(name="AgentSpace")
    builder.set_objective("Generate marketing assets on request.")
    builder.add_subagent(name="copywriter", task="Write marketing copy", tools=[])
    builder.add_subagent(name="designer", task="Create images", tools=[])
    agent = builder.build()
    result = agent.run(inputs={"request": "Create a launch email and banner for EcoShoeX"})
    print(result.output)

if __name__ == "__main__":
    main()
