#!/usr/bin/env bash
ROOT=$(pwd)

cd "${ROOT}" && cd 3.1.1.a* || exit
sh example_command.sh

cd "${ROOT}" && cd 3.1.1.b* || exit
sh example_command.sh

cd "${ROOT}" && cd 3.1.1.c* || exit
sh example_command.sh

cd "${ROOT}" && cd 3.1.1.d* || exit
python example_script.py

cd "${ROOT}" && cd 3.2.2.a* || exit
echo "Skip example 3.2.2.a"

cd "${ROOT}" && cd 3.2.3.a* || exit
sh example_command.sh

cd "${ROOT}" && cd 3.3.1.a* || exit
python example_get_data.py
python example_plot.py

cd "${ROOT}" && cd 3.3.1.b* || exit
sh example_command.sh

cd "${ROOT}" && cd 3.3.2.a* || exit
sh example_command.sh
python example_script-boltztrap2.py
python example_script-shengbte.py

cd "${ROOT}" && cd 3.3.3.a* || exit
python example_script.py

cd "${ROOT}" && cd 3.3.3.b* || exit
python example_script.py
