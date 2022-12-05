from pathlib import Path
import argparse

POSSIBLE_PROGRAMS = {"map-to-full-evid", "map-to-mmap-evid"}

arg_parser = argparse.ArgumentParser();
arg_parser.add_argument("--program", required=True, help="program to use to create an evidence file");
arg_parser.add_argument("--map-output-file", default="map.out", help="map output file");
arg_parser.add_argument("--mmap-query-file", default="mmap.query", help="mmap query file");
arg_parser.add_argument("--new-evidence-file", default="evidence.evid", help="resulting evidence file");


args = arg_parser.parse_args();

program = args.program
map_output_file = Path(args.map_output_file).absolute();
mmap_query_file = Path(args.mmap_query_file).absolute();
new_evidence_file = Path(args.new_evidence_file).absolute();

def map_to_full_evid():
    n_map_vars = None
    map_vars = None
    map_assignments = None
    tokens = None
    with map_output_file.open('r') as fin:
        tokens = []
        for line in fin:
            line = line.strip()
            if line == "":
                continue;
            temp_tokens = line.split()
            try:
                for t in temp_tokens:
                    int(t);
                tokens += temp_tokens;
            except(ValueError):
                continue;
    n_map_vars = int(tokens[0])
    assert(   
              ( n_map_vars == (len(tokens)-1) )
          or
              ( n_map_vars == ( (len(tokens)-1)//2) )
          )
    if( n_map_vars == (len(tokens)-1) ): # old UAI MPE format
        map_vars = list(range(n_map_vars))
        map_assignments = [int(x) for x in tokens[1:]]
    else: # UAI MMAP format
        map_vars = [int(x) for x in tokens[1::2]]
        map_assignments = [int(x) for x in tokens[2::2]]
    assert(len(map_vars) == len(map_assignments) == n_map_vars)
    map_assignment_tuples = dict(zip(map_vars,map_assignments))

    with new_evidence_file.open('w') as fout:
        print(n_map_vars, end=" ", file=fout)
        for i in map_vars:
            print(i, map_assignment_tuples[i], sep=" ", end=" ", file=fout)
        print(file=fout)



def map_to_mmap_evid():
    n_map_vars = None
    map_vars = None
    map_assignments = None
    tokens = None
    with map_output_file.open('r') as fin:
        tokens = []
        for line in fin:
            line = line.strip()
            if line == "":
                continue;
            temp_tokens = line.split()
            try:
                for t in temp_tokens:
                    int(t);
                tokens += temp_tokens;
            except(ValueError):
                continue;
    n_map_vars = int(tokens[0])
    assert(   
              ( n_map_vars == (len(tokens)-1) )
          or
              ( n_map_vars == ( (len(tokens)-1)//2) )
          )
    if( n_map_vars == (len(tokens)-1) ): # old UAI MPE format
        map_vars = list(range(n_map_vars))
        map_assignments = [int(x) for x in tokens[1:]]
    else: # UAI MMAP format
        map_vars = [int(x) for x in tokens[1::2]]
        map_assignments = [int(x) for x in tokens[2::2]]
    assert(len(map_vars) == len(map_assignments) == n_map_vars)
    map_assignment_tuples = dict(zip(map_vars,map_assignments))

    n_mmap_query_vars = None
    mmap_query_vars = None
    tokens = None
    with mmap_query_file.open('r') as fin:
        tokens = []
        for line in fin:
            line = line.strip()
            if line == "":
                continue;
            tokens += line.split()
    n_mmap_query_vars = int(tokens[0])
    mmap_query_vars = [int(x) for x in tokens[1:]]
    assert(len(mmap_query_vars) == n_mmap_query_vars)
    assert(n_mmap_query_vars <= n_map_vars)


    with new_evidence_file.open('w') as fout:
        print(n_mmap_query_vars, end=" ", file=fout)
        for i in mmap_query_vars:
            print(i, map_assignment_tuples[i], sep=" ", end=" ", file=fout)
        print(file=fout)


dispatcher = {
                "map-to-full-evid"  :   map_to_full_evid,
                "map-to-mmap-evid"  :   map_to_mmap_evid,
             }

assert(program in dispatcher)

dispatcher[program]()