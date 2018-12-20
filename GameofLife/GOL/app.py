from flask import Flask,render_template,request,redirect,session,url_for
import mlab
from models.activities import Activities
from models.friend import Friend
from models.habbit import Habbit
from models.posts import Post
from models.user import User
from models.contribute import Contribute
from models.attribute import Attribute
from models.quote import Quote
from models.all_history import All_history
import json


mlab.connect()

app = Flask(__name__)
app.config["SECRET_KEY"] = "qazqwsxcedcyhntyu"


@app.route("/sign_up", methods= ["GET", "POST"]) 
def sign_up():
    if request.method == "GET":
        return render_template("sign_up.html")
    else:
        form = request.form 
        fullname = form["fullname"]
        username = form["username"]
        email = form["email"]
        password = form["password"]
        confirm = form["confirm"]
        bday = form["bday"]
        gender = form["gender"]
        phone = form["telephone"]
        existUsername = User.objects(username= username).first()
        existEmail = User.objects(email= email).first()
        error = None

        if  fullname == "" or username == "" or email == "" or password == "" or confirm == "" or bday == "" or gender == "" or phone == "":
            error = "Bạn phải điền đầy đủ thông tin"
            return render_template("sign_up.html",error=error)
        elif existUsername is not None:
            error = "Tên đăng nhập đã tồn tại"
            return render_template("sign_up.html",error=error)
        elif len(username) < 8:
            error = "Tên người dùng không khả dụng"
            return render_template("sign_up.html",error=error)
        elif len(password) < 8:
            error = "Mật khẩu không khả dụng"
            return render_template("sign_up.html",error=error)
        elif confirm != password:
            error = "Rất tiếc. Xác nhận mật khẩu sai" 
            return render_template("sign_up.html",error=error)
        else :
            m = User(fullname= fullname, username= username, email= email, password= password, birthday= bday, gender= gender, phone= phone ,avt="https://cdn1.iconfinder.com/data/icons/ninja-things-1/1772/ninja-simple-512.png")
            m.save()  #Save
            att = Attribute(username = username)
            att.save()             
            hstr_list = All_history(user = username)
            hstr_list.save()
            Friend(username = username).save()
            
            return redirect("/sign_in")     



@app.route("/sign_in",methods=["GET","POST"])
def sign_in():
    if request.method == "GET":
        return render_template("sign_in.html")
    else:
        form = request.form 
        username = form["username"]
        password = form["password"] 
        found_user = User.objects(username= username).first()
        error = None
        if found_user is None:
            error = "Người dùng không tồn tại"
            return render_template("sign_in.html",error=error)
        elif found_user.password != password:
            error = "Mật khẩu sai"
            return render_template("sign_in.html",error=error)
        else:
            session["token"] = username #token
            return redirect(url_for("ca_nhan"))


@app.route("/logout")
def log_out():
    if "token" in session:
        del session["token"]
    return redirect(url_for("sign_in"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/social",methods=["GET","POST"])  
def social():
    user = Friend.objects(username=session["token"]).first()
    us = User.objects(username=session["token"]).first()
    friends = user.friend
    friend_post = []
    posts = Post.objects() 
    # commentss = []
    for post in posts:
        if post.user in friends:
            friend_post.append(post)
    # for post in friend_post:
    #     commentss.append(post.comments) 
    if request.method == "GET":
        return render_template("social.html",posts=friend_post,avt=us.avt) 
    else:
        form = request.form
        for i in form: 
            if "like" in i:
                like = form[i]
                if like != None:
                    for j in range(len(friend_post)): 
                        if str(j+1) in i: 
                            p = friend_post[j] 
                            if session["token"] not in p.wholike:
                                p.like += 1 
                                p.wholike.append(session["token"])
                            else:
                                p.like -= 1 
                                p.wholike.remove(session["token"])
                                
            else:
                comments =[]
                comment = {}
                comment["contain"] = form[i]
                comment["owner"] = session["token"]
                if comment["contain"] != None:
                    for j in range(len(friend_post)): 
                        if str(j+1) in i: 
                            p = friend_post[int(j)] 
                            p.comments.append(comment)
            p.save()
    return redirect(url_for("social"))


@app.route("/social/follow",methods=["GET","POST"])
def follow():
    error = None
    user = Friend.objects(username=session["token"]).first()
    friend_list = user.friend
    if request.method == "GET":
        return render_template("follow.html", friends=friend_list,name = session["token"],avt=user.avt)
    else:
        form = request.form
        search_friend = form["add_friend"]
        exist_user = Friend.objects(username=search_friend).first()
        if exist_user == None:
            error = "Không tìm thấy người dùng"
        elif exist_user.username == user.username:
            error = "Không thể tự theo dõi bản thân"
        elif exist_user.username in friend_list:
            error = "Đã theo dõi người dùng trước đó "
        else:
            friend_list.append(search_friend)
            user.save()
            error = "Thành công"
        return render_template("follow.html",error=error,friends = friend_list)
@app.route("/social/unfollow",methods=["GET","POST"])
def unfollow():
        user = Friend.objects(username=session["token"]).first()
        friend_list = user.friend
        if request.method == "GET":
            return render_template("unfollow.html", friends=friend_list,name = session["token"],avt=user.avt)
        else:
            form = request.form
            unf = form["unfollow"]
            friend_list.remove(unf)
            user.save()
            return redirect("/social/unfollow")

@app.route("/save_post",methods=["GET","POST"])
def save_share():
    if request.method == "GET":
        user = User.objects(username=session["token"]).first()
        return render_template("save_share.html",name = session["token"],avt=user.avt)
    else:
        form = request.form
        des = form["description"]
        img = form["image"]
        share = form["share"]
        if share == "yes":
            post = Post(img=img,user=session["token"],descript=des)
            post.save()
        All_history(img=img,user=session["token"],des=des).save()
        return redirect(url_for("ca_nhan"))


@app.route("/contribute", methods= ["GET", "POST"])
def contribute():
    if request.method == "GET":
        user = User.objects(username=session["token"]).first()
        return render_template("contribute.html",name = session["token"],avt=user.avt)
    else:
        form = request.form 
        user = session["token"]
        title = form["title"]
        st = form["STR"]
        per = form["PER"]
        knl = form["KNL"]
        soc = form["SOC"]
        cre = form["CRE"]
        ctb = Contribute(tit= title, st= st, per= per, knl= knl, soc= soc, cre= cre,user= user)
        ctb.save()
        mes = "Cảm ơn,chúng tôi sẽ xem xét góp ý của bạn"
        return render_template("contribute.html",mes=mes)


@app.route("/edit_information", methods= ["GET", "POST"]) 
def edit_information():
    user = User.objects(username= session["token"]).first() 
    if request.method == "GET":
        return render_template("edit_in4.html", user = user,name = session["token"],avt=user.avt)
    else:
        form = request.form 
        fullname = form["fullname"]
        email = form["email"]
        bday = form["bday"]
        gender = form["gender"]
        phone = form["telephone"]
        error = None   
        if  fullname == "" or email == "" or bday == "" or gender == "" or phone == "":
            error = "Bạn phải điền đầy đủ thông tin"
            return render_template("edit_in4.html", user = user,error=error)
        user.fullname = fullname
        user.email = email 
        user.birthday = bday
        user.gender = gender
        user.phone = phone 
        user.save() 
        return redirect(url_for("ca_nhan")) 

@app.route("/password1", methods= ["GET", "POST"])
def password1():
    user = User.objects(username= session["token"]).first() 
    if request.method == "GET":
        return render_template("password1.html", user = user,name = session["token"],avt=user.avt)
    else:
        form = request.form
        password = form["password"]
        error =None
        if password != user.password:
            error = "Sai mật khẩu. Hãy thử lại"
            return render_template("password1.html", user = user,error=error)
        else:
            return redirect(url_for("password2")) 

@app.route("/password2", methods= ["GET", "POST"])
def password2():
    user = User.objects(username= session["token"]).first() 
    if request.method == "GET":
        return render_template("password2.html",name = session["token"],avt=user.avt)
    else:
        form = request.form
        password = form["password"]
        confirm = form["confirm"]
        error =None
        if password == "" or len(password) < 8:
            error = "Vui lòng chọn mật khẩu dài hơn"
            return render_template("password2.html",error=error)
        elif confirm != password:
            error = "Mật khẩu không khớp"
            return render_template("password2.html",error=error)
        else:
            user.password = password
            user.save()
            return redirect(url_for("ca_nhan"))

@app.route("/ca_nhan", methods =["GET", "POST"])
def ca_nhan():
    
    if "token" in session:
        user = session["token"]
        info = User.objects(username = user).first()
        att = Attribute.objects(username = user).first()
        hstr_list = All_history.objects(user = user)
        qt_list = Quote.objects(username = user)
        my_data = {'field1': 'string value', 'field2': 100}
        if request.method == "GET":
            return render_template("ca_nhan.html", info = info, att = att, quotes = qt_list, history = hstr_list,name=user,avt=info.avt)
        else:
            form = request.form
            quote = form["quote"]
            author = form["author"]
            if author == "":
                q = Quote(username= user, quote = quote)
            else:
                q = Quote(username = user, quote = quote, author = author)
            q.save()
            return render_template("ca_nhan.html", info = info, att = att, quotes = qt_list, history = hstr_list)
    else:
        return redirect(url_for("sign_in"))
    
@app.route("/hoat-dong", methods = ["GET","POST"])
def hoat_dong():
    if request.method == "GET":
        user = User.objects(username=session["token"]).first()
        act_list = Activities.objects()
        return render_template("hoat_dong.html", act = act_list,name = session["token"],avt=user.avt)
    else:
        if "token" in session:
            user = session["token"]
            form = request.form
            act_list = Activities.objects()
            att_list = Attribute.objects(username = user).first()
            hstr_list = All_history.objects(user = user)

            for att in att_list:
                sort = form.get(att)
                if sort != None:
                    return redirect("/hoat-dong-sx-ttt-" + att)
                
            for act in act_list:
                action = form.get(act["tit"])
                if action != None:
                    for att in att_list :
                        if att in act and att != "id":
                            att_list[att] = att_list[att] + act[att]
                            if att_list[att] < 0:
                                att_list[att] = 0
                    att_list.save()
                    break                   
            return redirect("/save_post")
        else:
            return redirect(url_for("sign_in"))

@app.route("/hoat-dong-sx-ttt-<sort>", methods = ["GET", "POST"])
def hoat_dong_sx_ttt(sort):
    if request.method == "GET":
        user = User.objects(username=session["token"]).first()
        act_list = Activities.objects()
        return render_template("hoat_dong_sx_ttt.html", act = act_list, sort = sort,name = session["token"],avt=user.avt)
    else:
        if "token" in session:
            user = session["token"]
            form = request.form
            act_list = Activities.objects()
            att_list = Attribute.objects(username = user).first()
            hstr_list = All_history.objects(user = user).first

            toan_bo = form.get("all")
            if toan_bo != None:
                return redirect("/hoat-dong")

            for att in att_list:
                sort = form.get(att)
                if sort != None:
                    return redirect("/hoat-dong-sx-ttt-" + att)
                

            for act in act_list:
                action = form.get(act["tit"])
                if action != None:
                    hstr_list.tit.append(act["tit"])
                    for att in att_list :
                        if att in act and att != "id":
                            att_list[att] = att_list[att] + act[att]
                            if att_list[att] < 0:
                                att_list[att] = 0
                    att_list.save()
                    hstr_list.save()
                    break                   
            return render_template("hoat_dong_sx_ttt.html", act = act_list)
        else:
            return redirect(url_for("sign_in"))
            
            
if __name__ == '__main__':
  app.run(debug=True)
