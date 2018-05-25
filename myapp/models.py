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
    issue_proj =  db.Column(db.Integer)
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





