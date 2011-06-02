''' Define prior values for the documents
in the focused set, and for the docuemnts 
in the similar set.
'''
# boost = 1/5 (not real)
#prior_f = '-10.1832'
#prior_s = '-10.4757'
# boost = 1/3 (not real)
#prior_f = '-10.0778'
#prior_s = '-10.5565'
# boost = ~4
#prior_f = '-9.6723'
#prior_s = '-11.1032'
# boost = 2 (real)
prior_f = '-9.9528'
prior_s = '-10.6460'
# boost = 4 (real)
#prior_f = '-9.6580'
#prior_s = '-11.0442'

'''Write the prior values in the file, with
two columns separated by one white space: 
external docid and the prior value.'''

open('priorvalues','w').close()
with open('priorvalues','a') as f:
  for i in range(1,500):
    f.write(str(i)+' '+prior_f+'\n')
  for i in range(500,1105):
	f.write(str(i)+' '+prior_s+'\n')
  for i in range(1105,9157):
	    f.write(str(i)+' '+prior_f+'\n')
  for i in range(9909,11638):
    f.write(str(i)+' '+prior_f+'\n')
  for i in range(11638,32499):
    f.write(str(i)+' '+prior_s+'\n')
