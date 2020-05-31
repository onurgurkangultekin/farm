def index():
    pass


@auth.requires_login()
def save():
    profile_rows = db(db.profile.created_by == session.auth.user.id).select(orderby=~db.profile.id)
    for x in profile_rows:
        db.profile.farm_name.default = x.farm_name
        db.profile.farm_address.default = x.farm_address
        db.profile.farm_website.default = x.farm_website
        break
    form = SQLFORM(db.profile).process()
    return locals()
