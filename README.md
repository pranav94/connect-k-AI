# Project Connect K
## Install

Play against AI manually

`python3 src/connect-k-python/main.py {m} {n} {k} {g} m`

m=Columns, n=Rows, k=K, g=Gravity mode on/off (0/1), 'm' for manual mode

## Examples of playing against different AI with different parameters.

### Random AI
```
python3 tools/AI_runner.py 5 5 4 1 src/connect-k-python/main.py tools/SampleAI/RandomAI_v3.pyc
python3 tools/AI_runner.py 5 5 4 1  tools/SampleAI/RandomAI_v3.pyc src/connect-k-python/main.py

python3 tools/AI_runner.py 7 7 5 1 src/connect-k-python/main.py tools/SampleAI/RandomAI_v3.pyc
python3 tools/AI_runner.py 7 7 5 1 tools/SampleAI/RandomAI_v3.pyc src/connect-k-python/main.py

python3 tools/AI_runner.py 5 5 4 0 src/connect-k-python/main.py tools/SampleAI/RandomAI_v3.pyc

python3 tools/AI_runner.py 7 7 5 0 src/connect-k-python/main.py tools/SampleAI/RandomAI_v3.pyc
```

### Poor AI
```
python3 tools/AI_runner.py 5 5 4 1 src/connect-k-python/main.py tools/SampleAI/PoorAI_v2.pyc
python3 tools/AI_runner.py 5 5 4 1  tools/SampleAI/PoorAI_v2.pyc src/connect-k-python/main.py

python3 tools/AI_runner.py 7 7 5 1 src/connect-k-python/main.py tools/SampleAI/PoorAI_v2.pyc

python3 tools/AI_runner.py 7 7 5 1 tools/SampleAI/PoorAI_v2.pyc src/connect-k-python/main.py

python3 tools/AI_runner.py 5 5 4 0 src/connect-k-python/main.py tools/SampleAI/PoorAI_v2.pyc
python3 tools/AI_runner.py 7 7 5 0 src/connect-k-python/main.py tools/SampleAI/PoorAI_v2.pyc
```
