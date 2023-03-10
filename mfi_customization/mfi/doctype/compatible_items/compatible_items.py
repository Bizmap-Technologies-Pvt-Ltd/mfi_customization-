# Copyright (c) 2022, bizmap technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CompatibleItems(Document):
	pass


def add_item():
	compatible_items = frappe.get_all("Compatible Items")
	for c_item in compatible_items:
		c_item = frappe.get_doc("Compatible Items", c_item)
		if frappe.db.exists('Item',c_item.asset_item):
			item = frappe.get_doc('Item',c_item.asset_item)
			company = "MFI DOCUMENT SOLUTIONS KENYA"
			added_items = [row.item_code for row in item.items]
			added_compatible_toners = [row.item_code for row in item.compatible_toners]
			item_modified = 0
			if c_item.item not in added_items and c_item.type == "Accessories":
				print('*************adding Accessories***************')
				add_on_entry_child = item.append('items',{})
				add_on_entry_child.item_code = c_item.item
				add_on_entry_child.company = company
				add_on_entry_child.item_name = item.item_name
				add_on_entry_child.item_group = item.item_group
				add_on_entry_child.yeild = item.yeild
				item_modified = 1


			elif c_item.item not in added_compatible_toners and c_item.type == "Toner":
				print('*************adding Toner***************')
				add_on_entry_child = item.append('compatible_toners',{})
				add_on_entry_child.item_code = c_item.item
				add_on_entry_child.company = company
				add_on_entry_child.item_name = item.item_name
				add_on_entry_child.item_group = item.item_group
				add_on_entry_child.yeild = item.yeild
				item_modified = 1
			if item_modified:
				print('*************saving item***************')
				item.save()
				frappe.db.commit()

# def add_item_in_asset(doc, method):
# 	asset = frappe.get_doc("Asset", doc.asset)
# 	item = frappe.get_doc("Item", doc.item)

# 	if doc.type == "Accessories":
# 		items = [item.item_code for item in asset.items]
# 		if item.item_code not in items:
# 			row = asset.append('items', {})
# 			row.item_code = item.item_code
# 			row.item_name = item.item_name
# 			row.item_group = item.item_group
# 			row.yeild = item.yeild
# 	elif doc.type == "Toner":
# 		items = [item.item_code for item in asset.compatible_toners]
# 		if item.item_code not in items:
# 			row = asset.append('compatible_toners', {})
# 			row.item_code = item.item_code
# 			row.item_name = item.item_name
# 			row.item_group = item.item_group
# 			row.yeild = item.yeild
# 	asset.save()

