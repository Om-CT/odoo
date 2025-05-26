from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
import pytz
import re


class Employee(models.Model):
    _name = 'employee.management'
    _description = 'Employee Management'
    
    # _inherits={'res.partner':'officer_id'}
       
    roll_number=fields.Integer(string="Roll Number")
    checker=fields.Integer(string="Checker")
   
    _sql_constraints = [('roll_number_unique', 'unique(roll_number)', "The roll number is unique for each student.!"),
                        ('roll_number_check', 'check(checker > 0 )', "The roll number is greater than zero!")
                        ]
     

    utc_time = fields.Char(string="UTC Time", compute="_compute_times", store=False)
    dubai_time = fields.Char(string="Dubai Time", compute="_compute_times", store=False)
    india_time = fields.Char(string="India Time", compute="_compute_times", store=False)

    @api.depends()
    def _compute_times(self):
        for rec in self:
            utc_dt = datetime.utcnow()
            utc = pytz.timezone('UTC')
            utc_dt = utc.localize(utc_dt)

            dubai_dt = utc_dt.astimezone(pytz.timezone('Asia/Dubai'))
            india_dt = utc_dt.astimezone(pytz.timezone('Asia/Kolkata'))

            rec.utc_time = utc_dt.strftime('%Y-%m-%d %H:%M:%S')
            rec.dubai_time = dubai_dt.strftime('%Y-%m-%d %H:%M:%S')
            rec.india_time = india_dt.strftime('%Y-%m-%d %H:%M:%S')

    name = fields.Char(string='Employee Name', required=True)
    department = fields.Char(string='Department',trim=False)
    job_title = fields.Char(string='Job Title',translate=False)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    salary = fields.Float(string='Salary',digit=(16,2))
    bonus = fields.Float(string='Bonus')
    total_salary = fields.Float(string='Total Salary', compute='_compute_total_salary')
    age = fields.Integer(string='Age')
    is_adult = fields.Boolean(string='Is Adult')
    expi = fields.Integer(string='Experience')
    is_active = fields.Boolean(string='Is Active', default=True)
    address = fields.Text(string='Address')
    joining_date = fields.Date(string='Joining Date')
    last_login = fields.Datetime(string='Last Login')
    image = fields.Image(string="Photo",verify_resolution=True)
    last_update_time = fields.Datetime(string='Last Updated Time')
    officer_id = fields.Many2one('res.partner', string="Officer",ondelete="restrict")
    data_ids = fields.Many2many('employee.skill', string="Skills")
    job_history_ids = fields.One2many('employee.job.history', 'employee_id', string="Job History")
    research = fields.Many2many('employee.find', string="Find")
    employment_type = fields.Selection([
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('intern', 'Intern'),
    ], string='Employment Type', default='permanent')

    diff= fields.Html(string="Diff",strip_style=True)
    note = fields.Text(string="Note")  
      
   
    # ORM METHOD : CREATE
    def create_sample_employee(self):
        self.env['employee.management'].create({
            'name': 'jmt',
            'roll_number': 84,
            'email': 'jm123@gmail.com'
        })
    # BROWSE
    def browse_employee(self):
        employee = self.env['employee.management'].browse(186)
        employee.name = "jmt"

    # SEARCH
    def search_employees(self):
        employees = self.env['employee.management'].search([('roll_number', '=', 55)])
        print("employees,..",employees)

    # WRITE 
    def write_employee(self):
        employee = self.env['employee.management'].browse(186).write({'job_title':'odoo'})

    # unlink
    def delete_employee(self):
     employee= self.env['employee.management'].browse(193).unlink()
    
    # SEARCH COUNT
    def search_count_employee(self):
        count = self.env['employee.management'].search_count([('job_title', '=', 'odoo')])
        print("count..",count)

    #  get metadata
    def get_employee_metadata(self):
        employee = self.env['employee.management'].browse(7)  
        metadata = employee.get_metadata()
        print("metadata:",metadata)

    # get fields
    def get_field(self):
        field=self.env['employee.management'].fields_get()
        print("fields are:",field)
     
    # read 
    def read_field(self):
        field=self.env['employee.management'].browse(7)
        data = field.read(['name', 'email'])
        print(data)

    @api.depends('salary', 'bonus')
    def _compute_total_salary(self):
        for rec in self:
            rec.total_salary = rec.salary + rec.bonus

    @api.onchange('age')
    def _onchange_age(self):
        self.is_adult = self.age >= 18

    @api.constrains('email')
    def _check_email_format(self):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("Invalid email format: %s" % record.email)

    @api.constrains('phone')
    def _check_phone_format(self):
        phone_regex = r'^\+?\d{10,15}$'
        for record in self:
            if record.phone and not re.match(phone_regex, record.phone):
                raise ValidationError(f"Invalid phone number format: {record.phone}")

    def get_current_time(self):
        return fields.Datetime.now()

    def action_add_current_time(self):
        self.last_update_time = self.get_current_time()

    def mark_done_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Note',
            'res_model': 'wizard.mark.done',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_employee_id': self.id}
        }
    # override create method
    @api.model
    def create(self,vals):
        if not vals.get('job_title'):
            vals['job_title']='odoo'
        print("the create method")
        print("Before super create, self:", self)
        try:
            print("Before super create, self.name:", self.name)
        except Exception as e:
            print("Before super create, self.name error:", e)
        res=super(Employee,self).create(vals)
        print("res..",res)
        print("vals..",vals)
        print("After super create, res:", res)
        print("After super create, res.name:", res.name)
        return res
      
    def write(self, vals):  
        for record in self:
            print(f"\nBefore super write - self: {record}, self.name: {self.name}")
        
        result = super().write(vals)

        for record in self:
            print(f"After super write - self: {record}, self.name: {self.name}")

        return result

class WizardMarkDone(models.TransientModel):
    _name = 'wizard.mark.done'
    _description = 'Wizard to Edit Employee Note'

    employee_id = fields.Many2one('employee.management', string="Employee", required=True)
    note = fields.Text(string="Note")

    @api.model
    def default_get(self, fields):
        res = super(WizardMarkDone, self).default_get(fields)
        employee_id = self.env.context.get('default_employee_id')
        if employee_id:
            employee = self.env['employee.management'].browse(employee_id)
            res.update({
                'employee_id': employee.id,
                'note': employee.note
            })
        return res

    def mark_done(self):
        self.ensure_one()
        existing = self.env['employee.management'].search([
            ('id', '=', self.employee_id.id),
            ('note', '=', self.note)
        ])
        if not existing:
            self.employee_id.note = self.note
        return {'type': 'ir.actions.act_window_close'}





class EmployeeJobHistory(models.Model):
    _name = 'employee.job.history'
    _description = 'Employee Job History'

    name = fields.Char(string='Job Title', required=True)
    company = fields.Char(string='Company')
    years = fields.Integer(string='Experience')
    employee_id = fields.Many2one('employee.management', string='Employee')


class Skill(models.Model):
    _name = 'employee.skill'
    _description = 'Employee Skill'

    name = fields.Char(string="Skill Name")


class Find(models.Model):
    _name = 'employee.find'
    _description = 'Employee Find'

    name = fields.Char(string="Find Name")


