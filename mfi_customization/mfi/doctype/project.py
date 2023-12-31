# -*- coding: utf-8 -*-
# Copyright (c) 2020, bizmap technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import datetime ,timedelta, date
import calendar
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from frappe.model.mapper import get_mapped_doc
import json
import datetime
from datetime import datetime, timedelta
from frappe.model.document import Document

def get_company(doc,method):
    if doc.company:
        usr_perm = frappe.new_doc('User Permission')
        usr_perm.allow = 'Company'
        usr_perm.for_value = doc.company
        usr_perm.apply_to_all_doctypes = 1
        usr_perm.reference = doc.name
        if doc.users:
            for i in doc.users:
                if doc.company not in frappe.db.get_all('User Permission',{'allow':'Company','user':i.user},'for_value',pluck='for_value') or i.user not in frappe.db.get_all('User Permission',{'allow':'Company','for_value':doc.company},'user',pluck='user'):
                    usr_perm.user = i.user
                    usr_perm.save()
        else:
            if doc.name in frappe.db.get_all('User Permission','reference',pluck='reference'):
                us_per = frappe.get_doc('User Permission',{'reference':doc.name})
                frappe.delete_doc('User Permission', us_per.name)
            

def get_customer(doc,method):
    if doc.customer:
        usr_perm = frappe.new_doc('User Permission')
        usr_perm.allow = 'Customer'
        usr_perm.for_value = doc.customer
        usr_perm.apply_to_all_doctypes = 1
        usr_perm.reference = doc.name
        if doc.users:
            for i in doc.users:
                if doc.customer not in frappe.db.get_all('User Permission',{'allow':'Customer','user':i.user},'for_value',pluck='for_value') or i.user not in frappe.db.get_all('User Permission',{'allow':'Customer','for_value':doc.customer},'user',pluck='user'):
                    usr_perm.user = i.user
                    usr_perm.save()
                    user = frappe.get_doc("User", i.user)

                    # Add the role to the user's roles property
                    user.append("roles", {
                        "role": "Customer"
                    })

                    # Save the user document
                    user.save()
        else:
            if doc.name in frappe.db.get_all('User Permission','reference',pluck='reference'):
                us_per = frappe.get_doc('User Permission',{'reference':doc.name})
                frappe.delete_doc('User Permission', us_per.name)
                user = frappe.get_doc("User", us_per.user)
                print(f'\n\n\n{user.get("roles")}\n\n\n')
                role='Customer'
                for i in user.get("roles"):
                    if i.role == role:
                        user.remove_roles(role)
                        user.save()
                        print("\n\n\n\nRole '{}' removed from user '{}'\n\n\n".format(role, user.name))
                    else:
                        print("\n\n\nUser '{}' does not have the role '{}'\n\n\n".format(user.roles, role))
                # for i in user.get("roles"):
                #     if i.role == 'Customer':
                #         l.append(i.role)
                # if len(l)>0:
                #     user.set("roles", [role for role in user.roles if role.role not in l])
                #     user.save()

                # Save the user document
                # user.save()


def get_project(doc,method):
    if doc.project_name:
        usr_perm = frappe.new_doc('User Permission')
        usr_perm.allow = 'Project'
        usr_perm.for_value = doc.name
        usr_perm.apply_to_all_doctypes = 0
        usr_perm.applicable_for = 'Project'
        usr_perm.reference = doc.name
        if len(doc.users)>0:
            for i in doc.users:
                if doc.name not in frappe.db.get_all('User Permission',{'allow':'Project','user':i.user},'for_value',pluck='for_value') or i.user not in frappe.db.get_all('User Permission',{'allow':'Project','for_value':doc.name},'user',pluck='user'):
                    usr_perm.user = i.user
                    usr_perm.save()
        if len(doc.technician_team)>0:
            for i in doc.technician_team:
                if doc.name not in frappe.db.get_all('User Permission',{'allow':'Project','user':i.technician},'for_value',pluck='for_value') or i.technician not in frappe.db.get_all('User Permission',{'allow':'Project','for_value':doc.name},'user',pluck='user'):
                    usr_perm.user = i.technician
                    usr_perm.save()
        else:
            if doc.name in frappe.db.get_all('User Permission','reference',pluck='reference'):
                us_per = frappe.get_doc('User Permission',{'reference':doc.name})
                frappe.delete_doc('User Permission', us_per.name)

def get_tech_team(doc,method):
    if doc.project_name:
        usr_perm = frappe.new_doc('User Permission')
        usr_perm.allow = 'Project'
        usr_perm.for_value = doc.name
        usr_perm.apply_to_all_doctypes = 0
        usr_perm.applicable_for = 'Project'
        usr_perm.reference = doc.name
        if len(doc.technician_team)>0:
            for i in doc.technician_team:
                if doc.name not in frappe.db.get_all('User Permission',{'allow':'Project','user':i.technician},'for_value',pluck='for_value') or i.technician not in frappe.db.get_all('User Permission',{'allow':'Project','for_value':doc.name},'user',pluck='user'):
                    usr_perm.user = i.technician
                    usr_perm.save()
    # else:
    #     if doc.name in frappe.db.get_all('User Permission','reference',pluck='reference'):
    #         us_per = frappe.get_doc('User Permission',{'reference':doc.name})
    #         frappe.delete_doc('User Permission', us_per.name)


def make_issues_on_PM_call_interval():
   project_list = [p.get('name') for p in frappe.db.get_all('Project', 'name')]
   for project in project_list:
      project_doc = frappe.get_doc('Project', project)
      if project_doc.expected_end_date and project_doc.pm_call_interval > 0 and date.today() <= project_doc.expected_end_date:
         till_end_date = (project_doc.expected_end_date - project_doc.expected_start_date).days
         date_list = [project_doc.expected_start_date + timedelta(days=x) for x in range(0,till_end_date,project_doc.pm_call_interval)]
         if date.today() in date_list:
            for a in project_doc.machine_readings:
               if a.asset and not check_duplicate_issue(project_doc, a.asset):
                  issue_doc = frappe.new_doc('Issue')
                  issue_doc.subject = "PM Call Interval"
                  issue_doc.customer = project_doc.customer
                  issue_doc.asset = a.asset
                  issue_doc.location = frappe.get_value('Asset',{'name':a.asset},'location')
                  issue_doc.type_of_call = "PM"
                  issue_doc.issue_type = "Preventive"
                  issue_doc.failure_date_and_time = datetime.today()
                  issue_doc.raise_by_contact = frappe.get_value('Customer',{'name':project_doc.customer},'customer_name')
                  issue_doc.project = project_doc.name
                  issue_doc.status = "Open"
                  issue_doc.serial_no = frappe.get_value('Asset',{'name':a.asset},'serial_no')
                  issue_doc.area = frappe.get_value('Asset',{'name':a.asset},'area')
                  issue_doc.sub_location_area = frappe.get_value('Asset',{'name':a.asset},'sub_location_area')
                  issue_doc.machine_location = frappe.get_value('Asset',{'name':a.asset},'machine_location')
                  issue_doc.save()
                  print("Issue created for project", project_doc.name)

def check_duplicate_issue(doc, asset):
    return  frappe.db.get_all("Issue", filters={
            'subject' : "PM Call Interval",
            'customer' : doc.customer,
            'asset' : asset,
            'project':doc.name,
            'name': ['!=', doc.name]
        }, limit=1)


# @frappe.whitelist()
# def fetch_asset_maintenance_team(maintenance_team):
#     doc=frappe.get_doc('Asset Maintenance Team',maintenance_team)
#     resp={
#         'manager':doc.maintenance_manager,
#         'name':doc.maintenance_manager_name,
#     }
#     team=[]
#     for d in doc.get('maintenance_team_members'):
#         team.append({'member':d.get('team_member'),
#                     'name':d.get('full_name'),
#                     'role':d.get('maintenance_role')})
#     resp.update({'team_members_list':team})
#     return resp

# @frappe.whitelist()
# def make_asset_delivery_note(source_name, target_doc=None):
#     def set_missing_values(source,target):
#         if source.customer:
#             target.customer_name=frappe.db.get_value("Customer",source.customer,"customer_name")
#         if source.sales_order:
#             sales_order_doc=frappe.get_doc("Sales Order",source.sales_order)
#             for d in sales_order_doc.get("asset_quotation_selection"):
#                 if frappe.db.get_value("Item",d.asset,'is_fixed_asset'):
#                     target.append("asset_models",{
#                         "asset_model":frappe.db.get_value("Item",d.asset,'stock_item'),
#                         "model_name":d.asset_name,
#                         "qty":d.qty
#                     })
#     return get_mapped_doc("Project", source_name, {
#         "Project": {
#             "doctype": "Asset Delivery Note"
#         }
#     }, target_doc,set_missing_values)

# def validate(doc,method):
#     if doc.sales_order:
#         for d in frappe.get_all("Sales Order",{"name":doc.sales_order},['total_contract_amount']):
#             doc.estimated_costing=d.total_contract_amount

# @frappe.whitelist()
# def make_asset_task(doc):
#     doc = json.loads(doc)
#     existed_task_list = [t.name for t in frappe.db.get_all("Task", {'project': doc.get('name'), "type_of_call" :"Installation"} ,'name')]
#     if existed_task_list:
#         frappe.msgprint("Task <b>'{0}'</b> already exist.".format(",".join(map(str,existed_task_list))))
#     else:
#         asset_list = [a.name for a in frappe.db.get_all("Asset", {'project': doc.get('name')} ,'name')]
#         if asset_list :
#             out = []
#             for asset in asset_list:
#                 task_doc = frappe.new_doc("Task")
#                 task_doc.subject = "Installation-"+asset
#                 task_doc.type_of_call = "Installation"
#                 task_doc.project = doc.get('name')
#                 task_doc.completed_by = "s.karuturi@groupmfi.com"
#                 task_doc.customer= doc.get('customer')
#                 task_doc.save()
#                 out.append(task_doc)
#             return [p.name for p in out]

@frappe.whitelist()
def date_invoice_cycle(expected_end_date,invoicing_starts_from,invoice_cycle_option):
    monthlylist=[]
    yearlylist=[]
    quarterlylist =[]
    half_yearlist =[]
    endate=str(expected_end_date)
    endate_strp =datetime. strptime(endate, "%Y-%m-%d")
    endateformating = datetime(endate_strp.year,endate_strp.month,endate_strp.day)
    invoicing_start_date = str(invoicing_starts_from)
    invoicing_strp=datetime. strptime(invoicing_start_date,"%Y-%m-%d")
    invoce_startformating=datetime(invoicing_strp.year,invoicing_strp.month,invoicing_strp.day)
    [monthlylist.append(monthly.date()) for monthly in rrule.rrule(rrule.MONTHLY,dtstart=invoce_startformating,until=endateformating)]
    [yearlylist.append(yearly.date())for yearly in rrule.rrule(rrule.YEARLY,dtstart=invoce_startformating,until=endateformating)]
    if invoce_startformating> endateformating:
       frappe.throw("Invoicing Starts from date can't before Expected End Date")
    if invoice_cycle_option == "Quarterly":
       add_quarter_Months = relativedelta(months=3)
       while invoce_startformating <= endateformating:
          quarterlylist.append(invoce_startformating.date())
          invoce_startformating += add_quarter_Months
    if invoice_cycle_option == "Half Yearly":
       add_half_year_Month = relativedelta(months=6)
       while invoce_startformating <= endateformating:
          half_yearlist.append(invoce_startformating.date())
          invoce_startformating += add_half_year_Month


    return monthlylist,yearlylist,quarterlylist ,half_yearlist

@frappe.whitelist()
def contract_period(expected_start_date,contract_period):
    start_date=str(expected_start_date)
    start_strp=datetime. strptime(start_date,"%Y-%m-%d")
    stratformate=datetime(start_strp.year,start_strp.month,start_strp.day)
    current = stratformate + relativedelta(months=(int(contract_period)))
    return current.date()

@frappe.whitelist()
def customer_contect(customer):
   cus_contect = frappe.db.sql(f""" SELECT d.parent,c.email_id FROM `tabDynamic Link` d LEFT Join `tabContact` c on c.name = d.parent  WHERE d.link_name='{customer}' """, as_dict=True)
   return cus_contect



def get_customer_emails(project):
	emails = frappe.db.sql(f"""select distinct e.email_id from `tabProject` p, `tabCustomer Email List` e
									where e.parent="{project}" """, as_dict=1,)
	emails_list = [e['email_id'] for e in emails]

	return emails_list