import frappe
from frappe.model.document import Document

def get_company(doc,method):
    if doc.company not in frappe.db.get_all('User Permission',{'allow':'Company','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Company','for_value':doc.company},'user',pluck='user'):
        if doc.designation != 'Regional Technical Manager':
            print('\n\n\ncompjklkkllk\n\n\n\n')
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Company'
            usr_perm.for_value = doc.company
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
            # user_roles= frappe.get_roles(frappe.session.user)
            # if "Technician" in user_roles:
            user = frappe.get_doc("User", doc.user_id)

            # Add the role to the user's roles property
            user.append("roles", {
                "role": doc.designation
            })
            if doc.designation == 'Call Coordinator':
                user.append("roles", {
                "role": 'Sales Master Manager'
                })
                user.append("roles", {
                "role": 'System Manager'
                })

            if doc.designation == 'Technical Manager':
                user.append("roles", {
                "role": 'Purchase User'
                })
                user.append("roles", {
                "role": 'Stock User'
                })

            if doc.designation == 'Toner Coordinator':
                user.append("roles", {
                "role": 'System Manager'
                })

            # Save the user document
            user.save()

def get_user(doc,method):
   if doc.designation == 'Technicians':
       if doc.user_id:
           if doc.user_id not in frappe.db.get_all('User Permission',{'allow':'User','user':doc.user_id,'applicable_for':'Task'},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'User','for_value':doc.user_id,'applicable_for':'Task'},'user',pluck='user') or 'Task' not in frappe.db.get_all('User Permission',{'allow':'User','for_value':doc.user_id,'user':doc.user_id},'applicable_for',pluck='applicable_for'):
               usr_perm = frappe.new_doc('User Permission')
               usr_perm.user = doc.user_id
               usr_perm.allow = 'User'
               usr_perm.for_value = doc.user_id
               usr_perm.apply_to_all_doctypes = 0
               usr_perm.applicable_for = 'Task'
               usr_perm.save()
            

def get_territory(doc,method):
    if doc.territory:
        if (doc.territory not in frappe.db.get_all('User Permission',{'allow':'Territory','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Territory','for_value':doc.territory},'user',pluck='user')) and doc.designation != 'Regional Technical Manager':
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Territory'
            usr_perm.for_value = doc.territory
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
            # user_roles= frappe.get_roles(frappe.session.user)
            # if "Technician" in user_roles:
            user = frappe.get_doc("User", doc.user_id)

            # Add the role to the user's roles property
            user.append("roles", {
                "role": doc.designation
            })
            if doc.designation == 'Call Coordinator':
                user.append("roles", {
                "role": 'Sales Master Manager'
                    })
                user.append("roles", {
                "role": 'System Manager'
                })

            if doc.designation == 'Technical Manager':
                user.append("roles", {
                "role": 'Purchase User'
                })
                user.append("roles", {
                "role": 'Stock User'
                })

            if doc.designation == 'Toner Coordinator':
                user.append("roles", {
                "role": 'System Manager'
                })

                # Save the user document
            user.save()

def get_type_of_call(doc,method):
    if doc.type_of_call:
        if doc.type_of_call not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':doc.type_of_call},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = doc.type_of_call
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()

            user = frappe.get_doc("User", doc.user_id)

            # Add the role to the user's roles property
            user.append("roles", {
                "role": doc.designation
            })
            if doc.designation == 'Call Coordinator':
                user.append("roles", {
                "role": 'Sales Master Manager'
                })
                user.append("roles", {
                "role": 'System Manager'
                })

            if doc.designation == 'Technical Manager':
                user.append("roles", {
                "role": 'Purchase User'
                })
                user.append("roles", {
                "role": 'Stock User'
                })

            if doc.designation == 'Toner Coordinator':
                user.append("roles", {
                "role": 'Sales Master Manager'
                })

                # Save the user document
            user.save()
    if doc.designation == 'Call Coordinator':
        if 'CM' not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':'CM'},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = 'CM'
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
        if 'Ins' not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':'Ins'},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = 'Ins'
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
        if 'Kyocera Major incident' not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':'Kyocera Major incident'},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = 'Kyocera Major incident'
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
        if 'MFIcentral' not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':'MFIcentral'},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = 'MFIcentral'
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
        if 'MIS' not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':'MIS'},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = 'MIS'
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
        if 'MYQ' not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':'MYQ'},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = 'MYQ'
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
        if 'PM' not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':'PM'},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = 'PM'
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
        if 'Proprint' not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':'Proprint'},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = 'Proprint'
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
        if 'Proprint major incident' not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':'Proprint major incident'},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = 'Proprint major incident'
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()
        if 'Service Request' not in frappe.db.get_all('User Permission',{'allow':'Type of Call','user':doc.user_id},'for_value',pluck='for_value') or doc.user_id not in frappe.db.get_all('User Permission',{'allow':'Type of Call','for_value':'Service Request'},'user',pluck='user'):
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Type of Call'
            usr_perm.for_value = 'Service Request'
            usr_perm.apply_to_all_doctypes = 1
            usr_perm.save()

def get_locations(doc,method):
    if len(doc.locations)>0:
        frappe.log_error(f"locs,{frappe.db.get_all('User Permission',{'allow':'Location','user':doc.user_id},'for_value',pluck='for_value')}")
        l=[]
        r = []
        loc = []
        for i in doc.locations:
            # frappe.log_error(f'locs11111,{i}')
            if i.location not in frappe.db.get_all('User Permission',{'allow':'Location','user':doc.user_id},'for_value',pluck='for_value'):
                l.append(i.location)
        frappe.log_error(f'lll,{l}')
        for k in l:
            usr_perm = frappe.new_doc('User Permission')
            usr_perm.user = doc.user_id
            usr_perm.allow = 'Location'
            usr_perm.for_value = k
            usr_perm.apply_to_all_doctypes = 1
            frappe.log_error('SACEVEVE')
            usr_perm.save()

        for z in doc.locations:
            loc.append(z.location)


        for j in frappe.db.get_all('User Permission',{'allow':'Location','user':doc.user_id},'for_value',pluck='for_value'):
            frappe.log_error('REMOVE')
            if j not in loc:
                r.append(j)
                us_per = frappe.get_doc('User Permission',{'allow':'Location','user':doc.user_id,'for_value':j})
                frappe.delete_doc('User Permission', us_per.name)

def get_segment(doc,method):
    if doc.segment_type == 'Hardware':
        if len(doc.hardware_segment)>0:
            frappe.log_error(f"locs,{frappe.db.get_all('User Permission',{'allow':'Hardware Segment','user':doc.user_id},'for_value',pluck='for_value')}")
            l=[]
            r = []
            loc = []
            for i in doc.hardware_segment:
                # frappe.log_error(f'locs11111,{i}')
                if i.hardware_segment not in frappe.db.get_all('User Permission',{'allow':'Hardware Segment','user':doc.user_id},'for_value',pluck='for_value'):
                    l.append(i.hardware_segment)
            frappe.log_error(f'lll,{l}')
            for k in l:
                usr_perm = frappe.new_doc('User Permission')
                usr_perm.user = doc.user_id
                usr_perm.allow = 'Hardware Segment'
                usr_perm.for_value = k
                usr_perm.apply_to_all_doctypes = 1
                frappe.log_error('SAVE')
                usr_perm.save()

    elif doc.segment_type == 'Software':
        if len(doc.software_segment)>0:
            frappe.log_error(f"locs,{frappe.db.get_all('User Permission',{'allow':'Software Segment','user':doc.user_id},'for_value',pluck='for_value')}")
            l=[]
            r = []
            loc = []
            for i in doc.hardware_segment:
                # frappe.log_error(f'locs11111,{i}')
                if i.software_segment not in frappe.db.get_all('User Permission',{'allow':'Software Segment','user':doc.user_id},'for_value',pluck='for_value'):
                    r.append(i.software_segment)
            frappe.log_error(f'lll,{r}')
            for k in r:
                usr_perm = frappe.new_doc('User Permission')
                usr_perm.user = doc.user_id
                usr_perm.allow = 'Software Segment'
                usr_perm.for_value = k
                usr_perm.apply_to_all_doctypes = 1
                frappe.log_error('SAVE12')
                usr_perm.save()

def get_roles_checked(doc,method):  
    print('\n\n\nroles checkefd\n\n\n\n')
    if doc.designation == 'Regional Technical Manager':
        print('\n\n\ncompjklkkllk\n\n\n\n')
        user = frappe.get_doc("User", doc.user_id)
        user.append("roles", {
                "role": 'Regional Technical Manager'
        })
        user.append("roles", {
                "role": 'Projects Manager'
        })
        user.append("roles", {
        "role": 'Stock Manager'
        })
        user.save()

