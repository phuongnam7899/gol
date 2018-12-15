import mlab
from models.activities import Activities
from models.habbit import Habbit
mlab.connect()

activity = Activities(tit="tfhgbdvfc", per=1)
activity.save()

habbit = Habbit(tit="a" ,st=1 ,knl=1 ,cre= 1,per=1 ,soc=1 )
# habbit.save()
