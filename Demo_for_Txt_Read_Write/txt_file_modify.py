# ================================================================================
# for big *.txt file, modify some lines within file
# ================================================================================
fn = 'test_modify.txt'
key_words = 'str - 6'


def write_ref_file():
    with open(fn, 'w') as fid:
        info = ['str - ' + str(i) + '\n' for i in range(10)]
        fid.writelines(info)


def update_file():
    with open(fn, "r+") as fid:
        cursor = 0
        line = fid.readline()
        while line:
            if line.find(key_words) != -1:
                print(key_words)
                print(line)
                # read to end
                rest_part = fid.read()
                # seek to key line
                fid.seek(cursor)
                # delete the rest part
                fid.truncate()
                # update key line
                line += ' '.join([key_words]*5) + '\n'

                fid.write(line)
                fid.write(rest_part)
                break

            cursor = fid.tell() 
            line = fid.readline()

write_ref_file()
update_file()