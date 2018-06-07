import datetime
from myapp import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    __tablename_ = "users"
    user_email= db.Column(db.VARCHAR(40), nullable=False)
    user_name= db.Column(db.VARCHAR(30), nullable=False)
    user_password = db.Column(db.VARCHAR(200))
    user_empcode = db.Column(db.NVARCHAR(15), nullable=False, primary_key=True)
    user_approver_rights =  db.Column(db.Boolean, nullable=False)
    disbursements_approval_rights = db.Column(db.Boolean, nullable=False)

    responses = db.relationship("IssueResponse", lazy="dynamic", backref="user")
    

class Projects(db.Model):
    __tablename_ = "Projects"
    proj_id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    proj_manager = db.Column(db.NVARCHAR(20), db.ForeignKey("project_managers.manager_code"), nullable=False)
    proj_budget = db.Column(db.Numeric, nullable=False)
    proj_name = db.Column(db.NVARCHAR(40), nullable=False)
    proj_approval = db.Column(db.Boolean)
    proj_deadline = db.Column(db.DateTime)
    proj_hours = db.Column(db.Numeric)
    proj_client = db.Column(db.NVARCHAR(20), db.ForeignKey("clients.client_id"))
    proj_description = db.Column(db.NVARCHAR(1000))
    proj_type = db.Column(db.Integer, db.ForeignKey("project_types.type_id"))
    proj_currency = db.Column(db.Integer, db.ForeignKey("currency.curr_id"))
    proj_create_date = db.Column(db.Date, default=datetime.date.today, nullable=False)

    proj_disbs = db.relationship("ProjectDisbursements", lazy="dynamic", backref="project")
    proj_tasks = db.relationship("ProjectTasks", lazy="dynamic", backref="project")
    proj_material = db.relationship("WarehouseReqs", lazy="dynamic", backref="project")

class Clients(db.Model):
    __tablename_ = "clients"
    client_id = db.Column(db.NVARCHAR(20), primary_key=True)
    client_name = db.Column(db.NVARCHAR(40), nullable=False)
    project = db.relationship("Projects", backref="client", lazy="dynamic")

class Currency(db.Model):
    __tablename_ = "currency"
    curr_name = db.Column(db.NVARCHAR(10), nullable=False)
    curr_id = db.Column(db.Integer, primary_key=True)
    project = db.relationship(Projects, backref="currency", lazy="dynamic")

class ProjectTypes(db.Model):
    __tablename_ = "project_types"
    type_name = db.Column(db.VARCHAR(30), nullable=False)
    type_id = db.Column(db.Integer, primary_key=True)
    project = db.relationship("Projects", backref="type", lazy="dynamic")

class ProjectManagers(db.Model):
    __tablename_ = "project_managers"
    manager_email = db.Column(db.VARCHAR(40), nullable=False)
    manager_name = db.Column(db.VARCHAR(30), nullable=False)
    manager_code = db.Column(db.NVARCHAR(20), primary_key=True)
    project = db.relationship("Projects", backref="manager", lazy="dynamic")

class ProjectIssues(db.Model):
    __tablename_ = "project_issues"
    issue_proj =  db.Column(db.Integer, db.ForeignKey(Projects.proj_id))
    issue_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    issue_title = db.Column(db.VARCHAR(40), nullable=False)
    issue_descr =  db.Column(db.VARCHAR(10000), nullable=True)
    issue_date = db.Column(db.Date, nullable=False, default=datetime.date.today)
    responses = db.relationship("IssueResponse", lazy="dynamic", backref="issue")

class IssueResponse(db.Model):
    __tablename_ = "issue_response"
    issue_id = db.Column(db.Integer,  db.ForeignKey(ProjectIssues.issue_id), nullable=False)
    response_id = db.Column(db.Integer, nullable=False, primary_key=True)
    issue_responder = db.Column(db.NVARCHAR(15), db.ForeignKey(Users.user_empcode), nullable=False)
    issue_response =  db.Column(db.VARCHAR(10000), nullable=True)
    response_date = db.Column(db.Date, default=datetime.date.today, nullable=False)


class ProjectDisbursements(db.Model):
    __tablename_ = "project_disbursements"
    disb_id = db.Column(db.Integer, primary_key=True)
    disb_amt = db.Column(db.VARCHAR(30), nullable=False)
    disb_approver = db.Column(db.NVARCHAR(20))
    disb_status = db.Column(db.Boolean)
    disb_desc = db.Column(db.VARCHAR(10000), nullable=False)
    disb_proj = db.Column(db.Integer, db.ForeignKey(Projects.proj_id))
    disb_date = db.Column(db.DateTime, default=datetime.datetime.today, nullable=False)

class ProjectTasks(db.Model):
    __tablename_ = "project_tasks"
    task_proj = db.Column(db.Integer, db.ForeignKey(Projects.proj_id))
    task_id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.VARCHAR(30), nullable=False)
    task_desc = db.Column(db.VARCHAR(10000), nullable=False)
    task_start = db.Column(db.Date)
    task_deadline = db.Column(db.Date)
    task_hours = db.Column(db.Numeric, nullable=False)
    completion_status = db.Column(db.Numeric)
    task_issue_date = db.Column(db.DateTime, default=datetime.datetime.today, nullable=False)



###### Warehouses Models ########
class WarehouseUsers(db.Model):
    __tablename_ = "warehouse_users"
    user_email = db.Column(db.VARCHAR(200))
    user_password = db.Column(db.VARCHAR(200))
    user_empcode = db.Column(db.NVARCHAR(15), nullable=False, primary_key=True)
    user_approver_rights =  db.Column(db.Boolean, nullable=False)
    ####
    receipts = db.relationship("WarehouseReceipts", lazy="dynamic", backref="user")
    products = db.relationship("WarehouseProducts", lazy="dynamic", backref="user")
    requisitions = db.relationship("WarehouseReqs", lazy="dynamic", backref="requestor")
    categories = db.relationship("WarehouseCategories", lazy="dynamic", backref="creator")

class WarehouseReceipts(db.Model):
    __tablename_ = "warehouse_receipts"
    receipt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    receipt_date = db.Column(db.DateTime, default=datetime.datetime.today,  nullable=False)
    receipt_description = db.Column(db.VARCHAR(5000), nullable=False)
    receipt_product = db.Column(db.NVARCHAR(10), nullable=False)
    receipt_supplier = db.Column(db.VARCHAR(10), nullable=False)
    receipt_receiver = db.Column(db.NVARCHAR(15), db.ForeignKey(WarehouseUsers.user_empcode))
    receipt_qty = db.Column(db.Numeric, nullable=False)
    receipt_barcode= db.Column(db.VARCHAR(40), nullable=True)
    receipts_warehouse = db.Column(db.Integer, nullable=False)
    receipt_total_cost = db.Column(db.Numeric, nullable=False)
    receipt_document_no = db.Column(db.DateTime, default=datetime.datetime.today, nullable=False)

class WarehouseSuppliers(db.Model):
    __tablename_ = "warehouse_suppliers"
    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_Creation_date = db.Column(db.DateTime, default=datetime.datetime.today,  nullable=False)
    supplier_name = db.Column(db.VARCHAR(60), nullable=False)

class WarehouseProducts(db.Model):
    __tablename_ = "warehouse_products"
    product_id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.VARCHAR(60), nullable=False)
    product_type = db.Column(db.Integer, db.ForeignKey("warehouse_categories.cat_id"), nullable=False)
    product_creator = db.Column(db.NVARCHAR(15), db.ForeignKey("warehouse_users.user_empcode"))
    product_reorder = db.Column(db.Numeric, nullable=False)
    product_approver = db.Column(db.NVARCHAR(15))
    product_units = db.Column(db.Integer, db.ForeignKey("warehouse_units.units_id"), nullable=False)

    requisitions = db.relationship("WarehouseReqs", lazy="dynamic", backref="product")

### Both Warehouse and Project Module #####
class WarehouseReqs(db.Model):
    __tablename_ = "warehouse_reqs"
    req_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    req_date = db.Column(db.DateTime, default=datetime.datetime.today,  nullable=False)
    req_description = db.Column(db.VARCHAR(5000), nullable=False)
    req_product = db.Column(db.Integer, db.ForeignKey(WarehouseProducts.product_id), nullable=False)
    req_project = db.Column(db.Integer, db.ForeignKey(Projects.proj_id), nullable=False)
    req_requestor = db.Column(db.NVARCHAR(15), db.ForeignKey(WarehouseUsers.user_empcode))
    req_qty = db.Column(db.Numeric, nullable=False)
    #req_document_no = db.Column(db.DateTime, default=datetime.datetime.today, nullable=False)
    req_deadline = db.Column(db.DateTime, nullable=False)
    req_approval=db.Column(db.Boolean, default=False, nullable=True)
    req_approval_date = db.Column(db.DateTime,  nullable=True)


class WarehouseUnits(db.Model):
    __tablename_ = "warehouse_units"
    units_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    units_name = db.Column(db.VARCHAR(40), nullable=False)
    units_abbr = db.Column(db.NVARCHAR(15), nullable=False)

    product = db.relationship("WarehouseProducts", lazy="dynamic", backref="unitnames")

class WarehouseLocations(db.Model):
    __tablename_ = "warehouse_locations"
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.VARCHAR(40), nullable=False)
    location_lat = db.Column(db.Numeric, nullable=False)
    location_long = db.Column(db.Numeric, nullable=False)

    receipts = db.relationship("WarehouseReceipts", lazy="dynamic", backref="location")

class WarehouseCategories(db.Model):
    __tablename_ = "warehouse_categories"
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.VARCHAR(40), nullable=False)
    cat_creator = db.Column(db.NVARCHAR(15), db.ForeignKey(WarehouseUsers.user_empcode))
    
    products = db.relationship("WarehouseProducts", lazy="dynamic", backref="categoryNames")

##### generally needed Tables######
class Employees(db.Model):
    __tablename_ = "employees"
    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_name = db.Column(db.VARCHAR(60), nullable=False)
    emp_code = db.Column(db.NVARCHAR(15), nullable=False)
    emp_email = db.Column(db.VARCHAR(60), nullable=False)









