import survey

table = survey.Pregnancies()
table.ReadRecords()
print ('Number of pregnancies', len(table.records))

def life(data_dir):
    preg = survey.Pregnancies()
    preg.ReadRecords(data_dir)
    pregfirst = survey.Pregnancies()
    pregothers = survey.Pregnancies()
    prglenfirst = 0
    prglenothers = 0
    for record in preg.records:
        if record.outcome != 1:
            continue
        if record.birthord == 1:
            prglenfirst += record.prglength
            pregfirst.AddRecord(record)
        else:
            prglenothers += record.prglength
            pregothers.AddRecord(record)
    print('live birth: ', len(pregfirst) + len(pregothers))
    print('first prglength avg: ', prglenfirst/len(pregfirst))
    print('others prglength avg: ', prglenothers/len(pregothers))

def Summarize(data_dir):
    life(data_dir)


def main(name, data_dir='.'):
    Summarize(data_dir)


if __name__ == '__main__':
    import sys
    main(*sys.argv)