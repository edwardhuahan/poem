# usage: python run.py civil war

import os
import sys
import random
import subprocess as sp
import multiprocessing

scriptdir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(scriptdir)
py_dir = os.path.join(root_dir,"py")
exec_path = os.path.join(root_dir,'exec/./ZOPH_RNN_GPU_EXPAND') 
cwd=""


def post_process(lines):
    r = random.randint(1, 100000)
    before_path_tp = os.path.join(cwd, "before.txt")
    after_path_tp = os.path.join(cwd, "after.txt")
    before_path = before_path_tp + ".{}".format(r)
    after_path = after_path_tp + ".{}".format(r)

    f = open(before_path, 'w')
    for line in lines:
        f.write(line.strip() + "\n")
    f.close()
    
    cmd = "bash post_process.sh {} {}".format(before_path, after_path)
    sp.call(cmd.split(), cwd=py_dir)

    f = open(after_path)
    r = ""
    iline = 0
    for line in f:
        r += line
        iline += 1
        if iline % 4 == 0:
            r += "\n"
    f.close()
    os.remove(before_path)
    os.remove(after_path)
    return r


def process_poem(poem):
    ll = poem.split()[1:-1][::-1]
    newline = "\n"
    newll = []
    for w in ll:
        if w in ['?', '!', '.', ',']:
            w += newline
        newll.append(w)

    lines = ' '.join(newll).split(newline)
    lines = [x.strip() for x in lines]
    #poem_str = post_process(lines)
    poem_str = "\n".join(lines)
    return poem_str

def process_results(fn):
    f = open(fn)
    poem = "Empty Poem!"
    for line in f:
        if line.startswith("<START>"):
            poem = process_poem(line)
    f.close()
    return poem

def cleanup(fns):
    for fn in fns:
        os.remove(fn)

def cleanup_lstm():
    for name in os.listdir(root_dir):
        if len(name) == 19 and name[4] == "-" and name[9] == "-" and name[14] == "-":
            path = os.path.join(root_dir,name)
            if os.path.isdir(path):
                for name2 in os.listdir(path):
                    path2 = os.path.join(path,name2)
                    os.remove(path2)
                os.removedirs(path)
                

def process(model_path,source_path,fsa_path, encourage_path, output_path, beam_size=50, encourage_weight = 1.0, withFSA = True, pretrain_legacy = True):

    # generate the poem
    if withFSA:
        cmd = [exec_path]
        cmd += "--adjacent-repeat-penalty -2.0 --repeat-penalty -3.0".split()
        cmd += ("-L 60 -b {}".format(beam_size)).split()
        if pretrain_legacy:
            cmd += "--legacy-model 1".split()
        
        cmd += ("-k 1 {} {}".format(model_path,output_path)).split()
        cmd += ("--fsa {}".format(fsa_path)).split()

        cmd += ("--encourage-list {} --encourage-weight {}".format(encourage_path, encourage_weight)).split()
        cmd += "--dec-ratio 0.0 100.0".split()
        cmd += "--decode-main-data-files {}".format(source_path).split()


    else:

        cmd = [exec_path]
        cmd += ("-L 60 -b {}".format(beam_size)).split()
        if pretrain_legacy:
            cmd += "--legacy-model 1".split()
        cmd += ("-k 1 {} {}".format(model_path,output_path)).split()
        cmd += "--dec-ratio 0.0 100.0".split()
        cmd += "--decode-main-data-files {}".format(source_path).split()

    print " ".join(cmd)
    
    env = {}
    env["OMP_NUM_THREADS"] = str(multiprocessing.cpu_count())

    os.system(" ".join(cmd))
#    p = sp.Popen(cmd,cwd=root_dir,stdout=sp.PIPE, stderr=sp.PIPE,env=env, shell=True)
#    out, err = p.communicate()
    
    #print out
    
    # postprocess the poem
    poem = process_results(output_path)

    # print the poem to STDOUT
    print poem.encode("utf8")

    return poem

def main():
    model_path = sys.argv[1]
    source_path = sys.argv[2]
    fsa_path = sys.argv[3]
    encourage_path = sys.argv[4]
    output_path = sys.argv[5]
    beam_size=int(sys.argv[6])
    withFSA_int=int(sys.argv[7])
    global cwd
    cwd = sys.argv[8]
    withFSA = True
    if withFSA_int == 0:
        withFSA = False

    process(model_path,source_path,fsa_path,encourage_path,output_path,beam_size,withFSA=withFSA)

if __name__ == "__main__":
    main()
