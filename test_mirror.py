import unittest,copy
from mirror import validate
class FeedTests(unittest.TestCase):
 def feed(self):return {'schema':1,'generatedAt':1000,'events':[{'id':'1','title':'Show','artist':'Artist','artistId':'ellacoustic','artistIndex':0,'start':1100,'end':1500}]}
 def test_preserves_upstream_timestamp(self):
  data=self.feed();self.assertIs(validate(data,1100),data);self.assertEqual(data['generatedAt'],1000)
 def test_stale_and_future(self):
  for stamp in (99,1401):
   data=self.feed();data['generatedAt']=stamp
   with self.assertRaises(ValueError):validate(data,1100)
 def test_malformed_interval_and_artist(self):
  for field,value in [('end',1100),('artistIndex',7),('artistIndex',True),('start',float('nan'))]:
   data=self.feed();data['events'][0][field]=value
   with self.assertRaises(ValueError):validate(data,1100)
 def test_invalid_container_and_schema(self):
  for data in ([],{'schema':True,'generatedAt':1000,'events':[]}):
   with self.assertRaises(ValueError):validate(data,1100)
if __name__=='__main__':unittest.main()
