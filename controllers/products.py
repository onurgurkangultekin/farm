@auth.requires_login()
def proc():
    prod_dict = {}
    product_rows = db(db.products).select()
    for x in product_rows:
        prod_dict[str(x.id)] = x.product_name
    date_ordered = str(request.now.year) + "-" + str(request.now.month) + "-" + str(request.now.day)
    qty = request.vars.qty
    product_id = request.vars.product_id
    user_id = session.auth.user.id
    sql = "INSERT INTO orders (product_id, user_id, qty, status, date_ordered) values "
    sql += "({},{},{},'{}','{}')".format(product_id, user_id, qty, "cart", str(date_ordered))
    r = db.executesql(sql)
    rows = db(db.orders.user_id == session.auth.user.id).select(
        orderby=~db.orders.id)
    return locals()


@auth.requires_login()
def post():
    profile_roles = db(db.profile.created_by == session.auth.user.id).select(orderby=~db.profile.id)
    for x in profile_roles:
        db.products.farm_name.default = x.farm_name
        db.products.farm_address.default = x.farm_address
        db.products.farm_website.default = x.farm_website
        break
    form = SQLFORM(db.products).process()
    return locals()


@auth.requires_login()
def myposts():
    rows = db(db.products.created_by == session.auth.user.id).select(
        orderby=db.products.status | ~db.products.id)
    return locals()


@auth.requires_login()
def update():
    is_valid = False
    row = db(db.products.id == request.args(0)).select()
    for x in row:
        if x.created_by == session.auth.user.id:
            is_valid = True
    if is_valid:
        record = db.products(request.args(0)) or redirect(URL('view'))
        form = SQLFORM(db.products, record)
        if form.process().accepted:
            response.flash = T("Record Updated")
        else:
            response.flash = T("Please complete the form.")
    return locals()


def view():
    user_dict = {}
    userrows = db(db.auth_user).select()
    for x in userrows:
        user_dict[x.id] = x.first_name + " " + x.last_name
    rows = db(db.products.status == 'active').select(orderby=~db.products.id)
    return locals()


def index():
    pass
