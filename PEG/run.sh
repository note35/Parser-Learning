# Step1: Clone CPython repo from github
git clone git@github.com:python/cpython.git

# Step2: Copy peg_generator from CPython repo
cp -r cpython/Tools/peg_generator/pegen .

# Step3: Generate Parser based on given grammar

## Uncomment to generate CPython c parser
# python3 -m pegen c cpython/Grammar/python.gram cpython/Grammar/Tokens -o c_parser.c

## Uncomment to generate CPython python parser
# python3 -m pegen python pegen/metagrammar.gram -o python_parser.py

## Generate customized python parser for basic calculator
python3 -m pegen python basic_calculator_ii.python.gram -o basic_calculator_ii.py
## Run the generated parser with test input
python3 basic_calculator_ii.py test_input.txt
