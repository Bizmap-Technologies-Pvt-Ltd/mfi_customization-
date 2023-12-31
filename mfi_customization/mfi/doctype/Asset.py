import frappe
from datetime import datetime, timedelta, date
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from frappe.core.doctype.user_permission.user_permission import user_permission_exists


def after_insert(doc, method):
    if len(frappe.get_all('Asset Serial No', {"serial_no": doc.serial_no}, ['name', 'asset'])) > 0:
        for d in frappe.get_all('Asset Serial No', {"serial_no": doc.serial_no}, ['name', 'asset']):
            if d.asset:
                frappe.throw("serial number already exist")
            else:
                asn = frappe.get_doc('Asset Serial No', d.name)
                asn.asset = doc.name
                asn.location = doc.location
                asn.save()

    else:
        asn = frappe.new_doc('Asset Serial No')
        asn.subject = doc.serial_no
        asn.serial_no = doc.serial_no
        asn.asset = doc.name
        asn.location = doc.location
        asn.save()

def get_asset_up(doc, method):
    if doc.technician:
        user_perm = frappe.db.get_all('User Permission', {'allow':'Asset', 'for_value':doc.name}, ['user', 'name'])
        if user_perm and user_perm[0]['user'] != doc.technician:
            frappe.delete_doc("User Permission", user_perm[0]['name'] )
            
        if doc.technician in frappe.db.get_all('Employee','user_id',pluck='user_id'):
            emp = frappe.get_doc('Employee',{'user_id':doc.technician})
            if doc.technician not in frappe.db.get_all('User Permission', {'allow':'Asset', 'for_value':doc.name},'user',pluck='user') or 'Asset' not in frappe.db.get_all('User Permission', {'user':doc.technician, 'for_value':doc.name},'allow',pluck='allow') or doc.name not in frappe.db.get_all('User Permission', {'user':doc.technician, 'allow':'Asset'},'for_value',pluck='for_value'):
                if emp.company == doc.company:
                    usr_perm = frappe.new_doc('User Permission')
                    usr_perm.user = doc.technician
                    usr_perm.allow = 'Asset'
                    usr_perm.for_value = doc.name
                    usr_perm.apply_to_all_doctypes = 1
                    usr_perm.save()

def update_submitted_assets():
    ass = frappe.db.get_all('Asset',{'docstatus':1}, pluck='name')
    ass = ass[15002:20001]
    frappe.log_error(f'Asset,{ass}')
    for i in ass:
        frappe.log_error(f'Asset,{i}')
        ass_doc = frappe.get_doc('Asset', i)
        ass_doc.save()

@frappe.whitelist()   
def get_pm_date(creation, pm_call_interval,doc):
    import json
    doc = json.loads(doc)
    frappe.log_error('PM')
    today = creation
    return (datetime.today() + timedelta(days=int(pm_call_interval))).strftime('%Y-%m-%d')
    

def on_cancel(doc, method):
    # removing serial number on serial number
    frappe.db.delete('Asset Serial No', {'name': doc.serial_no})


def on_update(doc, method):
    # updating location in Serial No doctype with Asset location change.
    frappe.db.set_value('Asset Serial No', doc.serial_no,
                        'location', doc.location)


# @frappe.whitelist(allow_guest=True)
def make_task_on_PM_call_interval():
    today = datetime.today().strftime('%Y-%m-%d')
    asset_all = frappe.db.get_all('Asset', {'status':"Submitted"}, pluck='name')
    for i in asset_all:
        asset = frappe.get_doc('Asset',i)
        if len(asset.pm_schedule)>0:
            for i in asset.pm_schedule:
                if i.date == today:
                    project = frappe.get_value('Project', {'name': asset.project}, 'status')
                    if project == "Open":
                        if asset.serial_no not in frappe.db.get_all('Task',{'asset':asset.name},'serial_no',pluck='serial_no') or asset.name not in frappe.db.get_all('Task',{'serial_no':asset.serial_no},'asset',pluck='asset'):
                            task_doc = frappe.new_doc('Task')
                            task_doc.subject = "PM Call Interval"
                            task_doc.customer = frappe.get_value(
                                'Project', {'name': asset.project}, 'customer')
                            task_doc.asset = asset.name
                            task_doc.location = asset.location
                            task_doc.type_of_call = "PM"
                            task_doc.issue_type = "Preventive"
                            task_doc.failure_date_and_time = datetime.today()
                            task_doc.raise_by_contact = frappe.get_value(
                                'Customer', {'name': task_doc.customer}, 'customer_name')
                            task_doc.project = asset.project
                            task_doc.status = "Open"
                            task_doc.serial_no = asset.serial_no
                            task_doc.area = asset.area
                            task_doc.sub_location_area = asset.sub_location_area
                            task_doc.machine_location = asset.machine_location
                            task_doc.completed_by = asset.technician
                            task_doc.save()

        else:
            today1 = datetime.today().date()
            frappe.log_error('ELSEE')
            if asset.pm_call_interval:
                if asset.pm_date == today1:
                    project = frappe.get_value('Project', {'name': asset.project}, 'status')
                    if project == "Open":
                        if asset.serial_no not in frappe.db.get_all('Task',{'asset':asset.name},'serial_no',pluck='serial_no') or asset.name not in frappe.db.get_all('Task',{'serial_no':asset.serial_no},'asset',pluck='asset'):
                            task_doc = frappe.new_doc('Task')
                            task_doc.subject = "PM Call Interval"
                            task_doc.customer = frappe.get_value(
                                'Project', {'name': asset.project}, 'customer')
                            task_doc.asset = asset.name
                            task_doc.location = asset.location
                            task_doc.type_of_call = "PM"
                            task_doc.issue_type = "Preventive"
                            task_doc.failure_date_and_time = datetime.today()
                            task_doc.raise_by_contact = frappe.get_value(
                                'Customer', {'name': task_doc.customer}, 'customer_name')
                            task_doc.project = asset.project
                            task_doc.status = "Open"
                            task_doc.serial_no = asset.serial_no
                            task_doc.area = asset.area
                            task_doc.sub_location_area = asset.sub_location_area
                            task_doc.machine_location = asset.machine_location
                            task_doc.completed_by = asset.technician
                            frappe.log_error('CREATE')
                            task_doc.save()


@frappe.whitelist()
def date_pm_cycle(pm_cycle,project):

    invoicing_starts_from = frappe.get_value('Project', {'name': project}, 'expected_start_date')
    expected_end_date = frappe.get_value('Project', {'name': project}, 'expected_end_date')

    monthlylist=[]
    bymonthlylist=[]
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

    if pm_cycle == "By Monthly":
       add_By_Month = relativedelta(months=2)
       while invoce_startformating <= endateformating:
          bymonthlylist.append(invoce_startformating.date())
          invoce_startformating += add_By_Month

    if pm_cycle == "Quarterly":
       add_quarter_Months = relativedelta(months=3)
       while invoce_startformating <= endateformating:
          quarterlylist.append(invoce_startformating.date())
          invoce_startformating += add_quarter_Months

    if pm_cycle == "Half Yearly":
       add_half_year_Month = relativedelta(months=6)
       while invoce_startformating <= endateformating:
          half_yearlist.append(invoce_startformating.date())
          invoce_startformating += add_half_year_Month
    
    return monthlylist,yearlylist,quarterlylist,half_yearlist,bymonthlylist

@frappe.whitelist(allow_guest=True)
def share_doc_till_limit(doc, method=None):
    today = datetime.today().strftime('%Y-%m-%d')
    today= datetime.strptime(today, '%Y-%m-%d')
    user_list =[u['name'] for u in frappe.get_list("DocShare", {'share_doctype':"Asset",'share_name': doc.name}, 'name')]
    if len(user_list) > 0 and  doc.shared_till:
        time_limit = doc.creation + timedelta(hours=doc.shared_till)
        for user in user_list:
            if time_limit < today :
                frappe.db.sql("""delete from `tabDocShare` where name=%s""", user, debug=1)

