import sys
from process import apply_fx

fx = sys.argv[1]
dir_unproc = "/home/mike/workspace/lunapic/unprocessed/" + sys.argv[2] + "/"
dir_proc = "/home/mike/workspace/lunapic/processed/" + sys.argv[2] + "/" + fx + "/"

print(fx)
print(dir_unproc)
print(dir_proc)

apply_fx(fx, dir_unproc, dir_proc)
