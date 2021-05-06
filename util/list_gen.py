with open('input2', 'r') as a:
  with open('output_list_cb', 'w') as b:
    num = 0
    for line in a:
      line = line.strip().split()
      if num % 16 == 0:
        b.write('\t# cb {}\n'.format(hex(num)))
      b.write('\t{},\n'.format(line[0]))
      num += 1