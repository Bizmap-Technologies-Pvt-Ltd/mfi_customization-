cur_frm.dashboard.add_transactions([
	{
		'items': [
			'Asset',
			'Asset Maintenance',
			'Asset Maintenance Log',
			'Asset Repair'
		],
		'label': 'Others'
	},
]);



frappe.ui.form.on('Project', {
	setup:function(frm){
		frm.set_query("asset", "machine_readings", function() {
			var asset_list=[]
			cur_frm.doc.asset_list.map((value) => {
				asset_list.push(value.asset)
			})
			return {
				filters: {
					"name": ['in',asset_list]
				}
			}
		});
	}
})

frappe.ui.form.on("Asset List", "asset", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.db.get_value("Asset", {"name":d.asset},["asset_name"], function(r){
		d.asset_name=r.asset_name
		refresh_field("asset_list");
	})
});

frappe.ui.form.on("Asset Readings", "asset", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.db.get_value("Asset", {"name":d.asset},["asset_name"], function(r){
		d.asset_name=r.asset_name
		refresh_field("asset_list");
	})
});

// frm.set_query('document_type', () => {
// 	let invalid_doctypes = frappe.model.core_doctypes_list;
// 	invalid_doctypes.push('Accounting Dimension', 'Project',
// 		'Cost Center', 'Accounting Dimension Detail');

// 	return {
// 		filters: {
// 			name: ['not in', invalid_doctypes]
// 		}
// 	};
// });

