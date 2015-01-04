========
Usage
========

Basic::

  from dgim.dgim import Dgim
  dgim = Dgim(N=32)
  for i in range(100):
      dgim.update(True)
  print "Number of 'True' statements in the last 32 elements"
  exact_result = 32
  print "- Exact result : {}".format(exact_result)
  dgim_result = dgim.get_count() # 28
  print "- Dgim estimation: {}".format(dgim_result)


Custom error rate::

  from dgim.dgim import Dgim
  dgim = Dgim(N=32, error_rate=0.1)
  for i in range(100):
      dgim.update(True)
  print "Number of 'True' statements in the last 32 elements"
  exact_result = 32
  print "- Exact result : {}".format(exact_result)
  dgim_result = dgim.get_count() # 30
  print "- Dgim estimation: {}".format(dgim_result)


