import json
import argparse

def main(dataset_path: str):
    try:
        with open(dataset_path, 'r') as f:
            data = json.load(f)
        print(f"Loaded dataset with {len(data['samples'])} samples")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", required=True)
    args = parser.parse_args()
    main(args.dataset_path)
