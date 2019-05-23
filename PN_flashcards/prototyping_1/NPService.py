def get_names_memos_for(with_memo_file_path: str):
    Records_Container = {}
    try:
        with open(with_memo_file_path, 'r') as memo:
            for line in memo.readlines():
                line = line.split('\t')
                # print(line)
                assert(len(line) == 2)
                Records_Container[line[0].strip()] = line[1].strip()
    except Exception as e:
        Records_Container = {}
        pass
    return Records_Container


if __name__ == '__main__':
    import sys
    import os
    Resources_Directory = 'Resources'
    Event_Directory = 'CAS Diversity Heads'
    Target_Directory = os.path.join(Resources_Directory, Event_Directory)
    Memos_Path = os.path.join(Target_Directory, 'memos.ini')

    Records_Container = get_names_memos_for(Memos_Path)

    for filename in os.listdir(Target_Directory):
	    if filename.endswith('.png'):
	        filename = filename.split('.')[0]
	        if filename in Records_Container:
	            print(filename)
	            print(Records_Container[filename])
	    else:
	        continue
