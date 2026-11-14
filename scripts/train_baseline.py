from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.engine import train_baseline
if __name__ == '__main__':
    train_baseline()
    print('Baseline saved to models/baseline.joblib')
    print('Bundled dataset is synthetic demonstration data, not a real-world benchmark.')
