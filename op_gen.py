with open('input', 'r') as a:
  with open('output_op', 'w') as b:
    num = 0
    for line in a:
      line = line.strip()
      b.write('def {}():\n'.format(line))
      b.write('\t#{}\n'.format(hex(num)))
      b.write('\tpass\n\n')
      num += 1