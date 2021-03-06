import time, math

class ShimmerPos2():
   def __init__(self, distance=10.0):
      self.num = 2
      self.anchorDist = float(distance)
      self.dist = [0.0, 10.0]#[0.0] * self.num 
      self.x = 0.0
      self.y = 0.0
      self.x_curr = 0.0
      self.y_curr = 0.0
      self.x_last = [0.0]*5
      self.y_last = [0.0]*5
      return
   
   def update(self, client_str):
      if(len(client_str) == 7):  #correct length must be 7: 2 bytes id, 4 bytes distance, 1 byte end
         id = int(client_str[0])*10 + int(client_str[1])
         if id > self.num:
            print "device not in system"
            return  -1          
         distance = 0
         for i in range(4):
            distance *=10.0
            distance += int(client_str[2+i])            
         distance /= 100.0
         self.dist[id-1] = distance
         return  0
      else:
         return -1
   
   def sq(self, a):
      return a*a
      
   def calc(self):
      x_old = self.x
      y_old = self.y
      self.x_curr = (self.sq(self.anchorDist) + self.sq(self.dist[0]) - self.sq(self.dist[1]))/(2*self.anchorDist)
      a = self.sq(self.dist[0]) - self.sq(self.x_curr)
      if(a < 0):      
         self.x_curr = x_old
         self.y_curr = y_old
         return -1
      self.y_curr = math.sqrt(a)
      self.x_last[:-1] = self.x_last[1:]
      self.y_last[:-1] = self.y_last[1:]
      self.x_last[-1] = self.x_curr
      self.y_last[-1] = self.y_curr
      self.x = sum(self.x_last)/len(self.x_last)
      self.y = sum(self.y_last)/len(self.y_last)
      return 0
      
   def position(self):
      return (self.x, self.y)
      
      
if __name__ == "__main__":
   print __name__, "start ..."
   
   pos = ShimmerPos2(10.0)
   pos.update("010600\r")
   pos.update("020900\r")
   pos.calc()
   print "x = %f, y = %f" %pos.position()