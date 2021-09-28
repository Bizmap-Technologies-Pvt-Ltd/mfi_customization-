// Copyright (c) 2016, bizmap technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Request Template"] = {
	"filters": [
		{
			"label":"Company",
			"fieldname":"company",
			"fieldtype":"Link",
			"options":"Company",
			"reqd": 1
		},
		{
			"label":"Item Group",
			"fieldname":"item_group",
			"fieldtype":"Link",
			"options":"Item Group",
			"reqd": 0,
			on_change: () => {
				var item_group = frappe.query_report.get_filter_value('item_group');
				if (item_group){
					var item_group_list=frappe.query_report.get_filter_value('item_group_list');
					if (item_group_list){
					frappe.query_report.set_filter_value('item_group_list',item_group_list+','+item_group);
					}
					else{
					frappe.query_report.set_filter_value('item_group_list',item_group);
				}
				}
				
			}
		},
		{
			"fieldname":"item_group_list",
			"label": __("Item Group List"),
			"fieldtype": "Data",
			"read_only":1
		},
		{
			"label":"Brand",
			"fieldname":"brand",
			"fieldtype":"Link",
			"options":"Brand",
			"reqd": 0,
			on_change: () => {
				var brand = frappe.query_report.get_filter_value('brand');
				if (brand){
					var brand_list=frappe.query_report.get_filter_value('brand_list');
					if (brand_list){
					frappe.query_report.set_filter_value('brand_list',brand_list+','+brand);
					}
					else{
					frappe.query_report.set_filter_value('brand_list',brand);
				}
				}
				
			}
		},
		{
			"fieldname":"brand_list",
			"label": __("Brand List"),
			"fieldtype": "Data",
			"read_only":1
		},
		{
			"fieldname":"clear",
			"label": __("Clear Filter"),
			"fieldtype": "Button",
			onclick:()=>{
				frappe.query_report.set_filter_value('item_group_list','');
				frappe.query_report.set_filter_value('item_group','');
				frappe.query_report.set_filter_value('brand_list','');
				frappe.query_report.set_filter_value('brand','');
			}
		},
	]
};
