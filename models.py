from app import db

class ComplaintsCompanies(db.Model):
    __tablename__ = 'complaints-companies'

    complaint_id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String())
    company_response_user = db.Column(db.String())
    company_response_public = db.Column(db.String())
    was_response_timely = db.Column(db.String())
    date = db.Column(db.String())

    def __init__(self, complaint_id, company, company_response_user, 
    company_response_public, was_response_timely, date):
        self.complaint_id = complaint_id
        self.company = company
        self.company_response_user = company_response_user
        self.company_response_public = company_response_public
        self.was_response_timely = was_response_timely
        self.date = date

    def __repr__(self):
        return '<id {}>'.format(self.complaint_id)
    
    def serialize(self):
        return {
            'complaint_id': self.complaint_id, 
            'company': self.company,
            'company_response_user': self.company_response_user,
            'company_response_public':self.company_response_public,
            'was_response_timely': self.was_response_timely,
            'date': self.date
        }

class ComplaintsUsers(db.Model):
    __tablename__ = 'complaints-users'

    complaint_id = db.Column(db.Integer, primary_key=True)
    complaint_text = db.Column(db.Text())
    was_user_disputed = db.Column(db.String())
    date = db.Column(db.String())
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.issue_id'))

    def __init__(self, complaint_id, complaint_text, was_user_disputed, 
                 date, product_id, issue_id):
        self.complaint_id = complaint_id
        self.complaint_text = complaint_text
        self.was_user_disputed = was_user_disputed
        self.date = date
        self.product_id = product_id
        self.issue_id = issue_id

    def __repr__(self):
        return '<id {}>'.format(self.complaint_id)
    
    def serialize(self):
        return {
            'complaint_id': self.complaint_id,
            'complaint_text': self.complaint_text,
            'was_user_disputed': self.was_user_disputed,
            'date': self.date,
            'product_id': self.product_id,
            'issue_id': self.issue_id
        }

class Issues(db.Model):
    __tablename__ = 'issues'

    issue_id = db.Column(db.Integer, primary_key=True)
    main_issue = db.Column(db.String())
    sub_issue = db.Column(db.String())

    def __init__(self, issue_id, main_issue, sub_issue):
        self.issue_id = issue_id
        self.main_issue = main_issue
        self.sub_issue = sub_issue

    def __repr__(self):
        return '<id {}>'.format(self.issue_id)
    
    def serialize(self):
        return {
            'issue_id': self.issue_id,
            'main_issue': self.main_issue,
            'sub_issue': self.sub_issue
        }

class Products(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    main_product = db.Column(db.String())
    sub_product = db.Column(db.String())

    def __init__(self, product_id, main_product, sub_product):
        self.product_id = product_id
        self.main_product = main_product
        self.sub_product = sub_product

    def __repr__(self):
        return '<id {}>'.format(self.product_id)
    
    def serialize(self):
        return {
            'product_id': self.product_id,
            'main_product': self.main_product,
            'sub_product': self.sub_product
        }