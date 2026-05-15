import os

folders = [
    "src/agents/seo",
    "src/agents/writer",
    "src/agents/editor",
    "src/agents/designer",
    "src/graph",
    "src/database",
    "src/interface",
    "src/prompts",
    "src/schemas",
    "src/services",
    "src/utils",
    "data"
]

files = [
    "src/agents/seo/agent.py",
    "src/agents/seo/tasks.py",
    "src/agents/seo/__init__.py",
    "src/agents/writer/agent.py",
    "src/agents/writer/__init__.py",
    "src/agents/editor/agent.py",
    "src/agents/editor/__init__.py",
    "src/agents/designer/agent.py",
    "src/agents/designer/__init__.py",
    "src/agents/__init__.py",
    "src/graph/workflow.py",
    "src/graph/nodes.py",
    "src/graph/edges.py",
    "src/graph/state.py",
    "src/graph/__init__.py",
    "src/database/models.py",
    "src/database/repository.py",
    "src/database/sqlite.py",
    "src/database/__init__.py",
    "src/interface/app.py",
    "src/interface/__init__.py",
    "src/prompts/__init__.py",
    "src/schemas/state.py",
    "src/schemas/__init__.py",
    "src/services/__init__.py",
    "src/utils/__init__.py",
    "src/main.py",
    ".env"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Criado diretório: {folder}")

for file in files:
    with open(file, 'w') as f:
        pass
    print(f"Criado arquivo: {file}")
