# MCP_LEARNING

## Establishing the Analogy
Your client.py acts as a central Concierge Desk that manages highly specialized Experts (the servers) and a powerful Senior Concierge (the LLM/Agent) to process customer requests.



// **Phase 1: Setup and Initialization (Opening the Office)**
`This phase establishes the foundational structure and loads all necessary resources.`

                    [ Load .env (Check Vault) ]
                                 |
                                 v
                     [ Path Setup (Map Locations) ]
                                 |
                                 v
        [ MultiServerMCPClient Instantiation (HR & Logistics Dept) ]
                                 |
         +-----------------------+-----------------------+
         | Setup Math Expert (stdio Line) | Setup Weather Expert (stdio Line) |
         +-----------------------+-----------------------+
                                 | (Client manages both subprocesses)
                                 v
                      [ client.get_tools() (Compile Master Service Catalog) ]
                                 |
                                 v
                  [ Load LLM (Seat the Senior Concierge / The Brain) ]
                                 |
                                 v
                 [ create_react_agent (Hand over the SOP / Rulebook) ]

**Phase 2: Execution Workflow (Processing a Customer Request)**
`This phase visualizes the step-by-step process the Agent follows to answer a complex query using a tool.`
// Customer Request: What is the current weather in Mirpur Khas, Pakistan?

                      [ run_agent_test() Invoked (Quality Control Checker) ]
                                             |
                                             v
                           [ Agent/LLM (Senior Concierge) DECIDES ]
                           - "I cannot answer this."
                           - "I need the 'get_weather' tool."
                                             |
                                             v
                       [ Agent Formulates Tool Call (Formal Request) ]
                                             |
                                             v
                         [ MCP Client (Logistics) intercepts & Proxies ]
                                             |
                                             v
                  [ Internal Communication via stdio Phone Line to Weather Expert ]
                                             |
                                             v
        +--------------------------------------------------------------------------+
        | **Weather Server (Expert) Execution** |
        | 1. Receives the request.                                                 |
        | 2. Makes External API Call (OpenWeatherMap).                             |
        | 3. Returns result (e.g., 29.81°C) via stdio Line.                        |
        +--------------------------------------------------------------------------+
                                             |
                                             v
                          [ Agent receives Tool Result ]
                                             |
                                             v
                       [ Agent/LLM Formulates FINAL ANSWER ]
                       - "The current weather in Mirpur Khas... is 29.81°C."
                                             |
                                             v
                             [ Print Final Response (Final Report) ]
                                             |
                                             v
                                 [ End of Script / Cleanup ]
