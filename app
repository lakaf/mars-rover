# Shell script wrapper to run as module
export PYTHONPATH="$PYTHONPATH:$(cd "$(dirname "$0")" && pwd)"
python3 -m marsrover $@