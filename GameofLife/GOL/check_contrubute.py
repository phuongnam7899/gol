import mlab
from models.contribute import Contribute
from models.activities import Activities
from models.attribute import Attribute

mlab.connect()


contribute_list = Contribute.objects()
for contribute in contribute_list:
    print("title: ",contribute.tit)
    if contribute.st != 0:
        print("strength: ",contribute.st)
    if contribute.knl != 0:
        print("knowledge: ",contribute.knl)
    if contribute.per != 0:
        print("personality: ",contribute.per)
    if contribute.cre != 0:
        print("creative: ",contribute.cre)
    if contribute.st != 0:
        print("social: ",contribute.soc)
    choose = input("add?")
    if choose == "y":
        Activities(tit=contribute.tit,st=contribute.st,knl=contribute.knl,cre=contribute.cre,per=contribute.per,soc=contribute.soc).save()
        plus_user = Attribute.objects(username=contribute.user).first()
        plus_user.cre += 2
        plus_user.save()
        print("saved")
    contribute.delete()
    



    

