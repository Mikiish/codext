# The goal 
...is to create an extension for the agentic-AI orchestrator of OpenAI.
Ultimately, it would use codex-cli tool using onboarded models on big GPU cluster servers. The model would use OpenAI to orchestrate the work and delegate task to local models when it's possible. The main idea is to split tasks from high-level programming POV down to simple shell decisions that over-trained low-parameters models car run while being locally ran.

# Instructions

- You can install Codex-CLI using `npm install -g @openai/codex`
- You can and should rather try to compile it, so you can test modifications.
- Use the src-codex.sh script for that.
- When prompting a new sub-task to another agents, always direct theim into the relevant folder.
- Always ensure your sub-agents does not read further than n-1 (or n-2 if necessary) folders in the hierarchy.
- As an orchestrator, which you are because you're reading this file, you should always prompts your sub-agents to precise tasks to optimise token usages.
- Orchestrators are using o3-pro. Coding, Debugging and Ask agents are using gpt-4.1. Architects and Manager agents are using o4-mini.
- Do not use codex-cli to delegate tasks. Use it only for testes.
