with open('input', 'r') as a:
  with open('output_list', 'w') as b:
    num = 0
    for line in a:
      line = line.strip().split()
      b.write('\t({}, {}, {}),\t\t\t\t# 0x{}\n'.format(*line, num))
      num += 1