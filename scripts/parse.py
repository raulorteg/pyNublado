import argparse
import sys

sys.path.append('..')
sys.path.append('../src/')

from src.parser import OutputParser

if __name__ == "__main__":
    
    # example: python parse.py --N_sample=10
    # will parse all Cloudy runs within "../data/samples/sample_N10"
    parser = argparse.ArgumentParser()
    parser.add_argument("--N_sample", required=True, type=int,
                        help="Number of models in the sample. "
                             "Note: some parameter combinations will be filtered out due to not being physical)")
    args = parser.parse_args()
    path = f"../data/samples/sample_N{args.N_sample}"
    OutputParser().parse(path=path)
