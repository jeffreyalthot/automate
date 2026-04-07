from __future__ import annotations

from src.agent import Agent


def main() -> None:
    agent = Agent.create()
    print("Automate IA local prêt. Tape 'exit' pour quitter.")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        output = agent.run(user_input)
        print(output)


if __name__ == "__main__":
    main()
