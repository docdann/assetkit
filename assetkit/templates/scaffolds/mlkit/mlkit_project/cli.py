import argparse
from {{PROJECT_NAME}}.core import trainer

def main():
    parser = argparse.ArgumentParser(description="{{PROJECT_NAME}} CLI")
    parser.add_argument("command", choices=["train", "evaluate", "shell"], help="Command to run")
    args = parser.parse_args()

    if args.command == "train":
        print("[{{PROJECT_NAME}}] Starting training...")
        trainer.train()
    elif args.command == "evaluate":
        print("[{{PROJECT_NAME}}] Evaluation not implemented yet.")
    elif args.command == "shell":
        import code
        code.interact(local=globals())
