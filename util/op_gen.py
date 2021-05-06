with open('input2', 'r') as a:
  with open('output_op_cb', 'w') as b:
    num = 0
    for line in a:
      line = line.strip().split()
      b.write('def {}(cpu):\n'.format(line[0]))
      b.write('\t# cb {}\n'.format(hex(num)))
      b.write('\tpass\n\n')
      num += 1