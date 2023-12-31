frappe.ui.form.on('Issue', {
	customer:function(frm){
	 if(frm.doc.customer){
	        frappe.db.get_value('Customer',frm.doc.customer,'customer_name',(r)=>{
	            console.log("frm.doc.customer",frm.doc.customer)
	            console.log('rrrrrrrrrr',r)
	            console.log('customer_name',r.customer_name)
	            frm.set_value('name_of_the_customer',r.customer_name)
	           // frm.refresh_fields("name_of_the_customer");
	        })
	    }
	},
	onload:function(frm){
	    if((frappe.user.has_role("Technicians") == 1 || frappe.user.has_role("Toner Approval 1") == 1) && frappe.user!="Administrator"){
	        frm.set_df_property('symptoms',"reqd",1);
	        frm.set_df_property('action',"reqd",1);
	        frm.set_df_property('cause',"reqd",1);
	        frm.set_df_property('signature',"reqd",1);
	        frm.set_df_property('priority',"read_only",1);
	        frm.remove_custom_button('Close');

	    }
	    if((frappe.user.has_role("Call Coordinator") == 1 || frappe.user.has_role("Toner Coordinator") == 1) && frappe.user!="Administrator"){
	        frm.set_df_property('symptoms',"read_only",1);
	        frm.set_df_property('action',"read_only",1);
	        frm.set_df_property('cause',"read_only",1);
	        frm.set_df_property('signature',"read_only",1);
	        frm.set_df_property('current_reading',"hidden",1);
	        frm.set_df_property('priority',"read_only",0);
	    }
		cur_frm.dashboard.hide()
		     /*
			frappe.call({
			method: "mfi_customization.mfi.doctype.issue.get_logged_user",
			args: {

			},
			callback: function(r) {

			frm.set_value("customer",r.message);

			}


	      });
		*/
		if(frappe.user.has_role("Customer")==1 && frappe.user!="Administrator"){
            $(".form-assignments").hide();
		    $(".form-attachments").hide();
		    $(".form-shared").hide();
		    $(".form-tags").hide();
		    $(".form-sidebar-stats").hide();
		    $(".list-unstyled.sidebar-menu.text-muted").hide();
		    $(".prev-doc").hide();
	        $(".next-doc").hide();
            $(".menu-btn-group").hide();

            //frm.set_df_property('customer',"read_only",1);
            frm.set_df_property('current_reading',"hidden",1);
			// frm.set_df_property('toner_type', "reqd", 0);
            // frm.set_df_property('toner_type', "hidden", 1);

        }
		// if(frappe.user.has_role("Toner Coordinator")==1){
		// 	frm.set_df_property('toner_type', "hidden", 1);
		// }
	},

	before_save:function(frm){
		if(!frm.doc.first_responded_on && frm.doc.status == 'Closed'){
			frappe.throw("Status Cannot be Closed before working")
		}
	},
	raised_by: function ( frm ) {

	if (!(frappe.utils.validate_type(frm.doc.raised_by, "email")) && !(frappe.utils.validate_type(frm.doc.raised_by, "number"))) {
		frappe.msgprint('Please Enter valid email or contact');

	}
   },
   type_of_call: function (frm) {
		if(frm.doc.type_of_call && (frappe.user.has_role("Call Coordinator") != 1 || frappe.user.has_role("Toner Coordinator") != 1) && frappe.user=="Administrator" && frappe.user.has_role("Customer")!=1){
			frappe.db.get_value('Type of Call',{'name':frm.doc.type_of_call},'ignore_reading', (r) => {
				if(r.ignore_reading == 1){
					frm.set_df_property('current_reading','hidden',1);
				}
				else{
					frm.set_df_property('current_reading','hidden',0);
				}
			});
            if (frm.doc.project){
            	frappe.call({
					method: "mfi_customization.mfi.doctype.issue.check_type_of_call",
					args: {
						"project":frm.doc.project,
						"type_of_call":frm.doc.type_of_call
					},
				    callback: function(r) {
				        if(r.message){
					        frm.set_value('status', "Hold")
				        }
				    }
				});
            }

		}
   },
	serial_no:function(frm){
		if(frm.doc.serial_no){
		// frm.set_value('asset','');
		// frm.set_value('asset_name','');
		// frm.set_value('location','');
		// frm.set_value('customer','');
		if (frm.doc.serial_no && frm.doc.asset){
			frappe.call({
			method: "mfi_customization.mfi.doctype.issue.get_customer",
			args: {
				"serial_no":frm.doc.serial_no,
				"asset":frm.doc.asset
			},
			callback: function(r) {
					frm.set_value('customer',r.message);
				}
			});
		}

		frappe.db.get_value('Asset Serial No',{'name':frm.doc.serial_no},['asset','location'])
		.then(({ message }) => {

			if (!frm.doc.asset){
					frm.set_value('asset',message.asset);
				}

			if (!frm.doc.location){
					frm.set_value('location',message.location);
				}
		});
	}},
	clear:function(frm){
        frm.set_value('asset','');
        frm.set_value('location','');
        frm.set_value('serial_no','');
		// frm.set_value('customer','');
		frm.set_value('name_of_the_customer','');



},

	asset:function(frm){
		if (frm.doc.asset){
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Asset",
					filters: {name: frm.doc.asset}
				},
				callback: function(r) {
					if(r.message){
				       frm.set_value('asset_name',r.message.asset_name);
						frm.set_value('company',r.message.company);
						frm.set_value('serial_no',r.message.serial_no);
						frm.set_value('location',r.message.location);
					}
				}
			});
		if (frm.doc.serial_no && frm.doc.asset){
			frappe.call({
			method: "mfi_customization.mfi.doctype.issue.get_customer",
			args: {
				"serial_no":frm.doc.serial_no,
				"asset":frm.doc.asset
			},
			callback: function(r) {
					frm.set_value('customer',r.message);
				}
			});
		}
	}
		if (!frm.doc.asset){
			frm.set_value('asset_name','');
		}
	},
	status:function(frm){
		if(frm.doc.status == 'Closed'){
			if(frm.doc.type_of_call && (frappe.user.has_role("Call Coordinator") != 1 || frappe.user.has_role("Toner Coordinator") != 1) && frappe.user=="Administrator" && frappe.user.has_role("Customer")!=1){
                frappe.db.get_value('Type of Call',{'name':frm.doc.type_of_call},'ignore_reading', (r) => {
                    if(r.ignore_reading == 1){
                        frm.set_df_property('current_reading','hidden',1);
                    }
                    else{
                        frm.set_df_property('current_reading','hidden',0);
                        frm.set_df_property('current_reading','reqd',1);
                    }
                });
            }
			frm.set_value('closing_date_time',frappe.datetime.now_datetime());

		}
		if (!["Cancelled","Closed"].includes(frm.doc.status)){
			frm.add_custom_button(__('Cancel'), function() {
				frm.set_value("status","Cancelled")
				frm.save()
			})
		}
		if (["Cancelled","Closed"].includes(frm.doc.status)){
			frm.remove_custom_button("Cancelled");
		}
		if(frappe.user.has_role("Customer")==1 && frappe.user!="Administrator"){
            frm.set_value('status', "Open")
            frm.save()
        }
	},
	details_available:function(frm){
			if (!frm.doc.details_available){
				frm.set_df_property('asset','reqd',0);
				frm.set_df_property('serial_no','reqd',0);
				frm.set_df_property('asset','read_only',1);
				frm.set_df_property('serial_no','read_only',1);
				frm.set_df_property('location','reqd',0);
			}
			if(frm.doc.details_available){
				frm.set_df_property('asset','reqd',1);
				frm.set_df_property('serial_no','reqd',1);
				frm.set_df_property('asset','read_only',0);
				frm.set_df_property('serial_no','read_only',0);
			}
	},
	location:function(frm){
		if (frm.doc.location){
			frappe.db.get_value('Location',{'name':frm.doc.location},['company'])
			.then(({ message }) => {
				frm.set_value('company',message.company);
			});
		}

	},
	setup:function(frm){

		frm.set_query("issue_type", function() {
			return {
				query: 'mfi_customization.mfi.doctype.issue.get_issue_types',
				filters: {
					"type_of_call":frm.doc.type_of_call
			}
			}
		});
		// frm.set_query("asset", "current_reading", function() {

		// 	return {
		// 		filters: {
		// 			"name": frm.doc.asset || ""
		// 		}

		// }
		// });







		    frm.set_query("location", function() {
			return {
				query: 'mfi_customization.mfi.doctype.issue.get_locationlist',
				filters: {
					"Customer_Name":frm.doc.customer
			}
			}
		});





		frm.set_query("asset", function() {
			if (frm.doc.project) {
				return {
					query: 'mfi_customization.mfi.doctype.issue.get_asset_list',
					filters: {
						"location":frm.doc.location
					}
				};
			}
		});

		// frm.set_query("location", function() {
		// 	if (frm.doc.customer) {
		// 		return {
		// 			query: 'mfi_customization.mfi.doctype.issue.get_location',
		// 			filters: {
		// 				"customer":frm.doc.customer
		// 			}
		// 		};
		// 	}
		// });
		frm.set_query("asset", function() {
			if (frm.doc.customer && frm.doc.location) {
				return {
					query: 'mfi_customization.mfi.doctype.issue.get_asset_in_issue',
					filters: {
						"location":frm.doc.location,
						"customer":frm.doc.customer
					}
				};
			}
			if (frm.doc.customer && !frm.doc.location) {
				return {
					query: 'mfi_customization.mfi.doctype.issue.get_asset_on_cust',
					filters: {
						"customer":frm.doc.customer
					}
				};
			}

		});

		frm.set_query("serial_no", function() {
			if(frm.doc.location && frm.doc.asset){
			return {
					query: 'mfi_customization.mfi.doctype.issue.get_serial_no_list',
					filters: {
						"location":frm.doc.location
						,"asset":frm.doc.asset
					}
				};}
				if (frm.doc.customer && !frm.doc.location) {
					return {
						query: 'mfi_customization.mfi.doctype.issue.get_asset_serial_on_cust',
						filters: {
							"customer":frm.doc.customer
						}
					};
				}
				if(frm.doc.customer &&  frm.doc.location){
					return {
						query: 'mfi_customization.mfi.doctype.issue.get_serial_on_cust_loc',
						filters: {
							"location":frm.doc.location,
							"customer":frm.doc.customer
						}
					};

				}
		});

	},
	refresh: function (frm) {
		// if (frappe.user=="Administrator"){
		// 	frm.set_df_property('toner_type', "reqd", 0);
		// }
		// if (frm.doc.status == 'Task Completed'){

		// }
		hide_request_mtrl_stus(frm)
		status_read_oly_fr_call_cordinator(frm)
		cur_frm.dashboard.hide()
        frappe.db.get_value("Task", {"issue": frm.doc.name}, 'name',(r) =>{
			if(r.name){
				frm.set_df_property('status','read_only',1);
			}
		});
		if (!frm.doc.__islocal ){
			if (!["Cancelled","Closed"].includes(frm.doc.status) && frm.doc.status != 'Task Completed'){
				frm.add_custom_button(__('Cancel'), function() {
					frm.set_value("status","Cancelled")
					frm.save()
				})
			}

		frm.add_custom_button(__('Task'), function() {
			frappe.set_route('List', 'Task', {issue: frm.doc.name});
		},__("View"));
		// if (frm.doc.type_of_call=="Service Request" && frm.doc.issue_type=="Error message"){
		// 	frm.remove_custom_button("Task", 'Create')
		// 	frm.add_custom_button(__("Task"), function() {
		// 		frappe.model.open_mapped_doc({
		// 			method: "mfi_customization.mfi.doctype.issue.make_task",
		// 			frm: frm
		// 		});
		// 	}, __("Create"));
		// }
		if (frm.doc.status == "Hold"){
			frm.remove_custom_button("Task", 'Create')
		}

		if (frm.doc.status !== "Closed" && frm.doc.agreement_fulfilled === "Ongoing") {
			frm.remove_custom_button("Task", 'Make')
			frm.add_custom_button(__("Task"), function () {
				frappe.model.open_mapped_doc({
					method: "mfi_customization.mfi.doctype.issue.make_task",
					frm: frm
				});
			}, __("Make"));
		}
		if (frm.doc.status == "Closed" || frm.doc.status == "Task Completed"){
            if(frm.doc.type_of_call){
                frappe.db.get_value('Type of Call',{'name':frm.doc.type_of_call},'ignore_reading', (r) => {
                    if(r.ignore_reading == 1){
                        frm.set_df_property('current_reading','hidden',1);
                    }
                    else{
                        frm.set_df_property('current_reading','hidden',0);
                        frm.set_df_property('current_reading','read_only',1);
                    }
                });
            }
		}
	}
	else{
		frm.trigger('customer');
		frm.remove_custom_button('Task','Make');
		frm.remove_custom_button('Task','View');
		frm.remove_custom_button('Close');

	}
	if(frm.doc.details_available){
		frm.set_df_property('asset','reqd',1);
		frm.set_df_property('serial_no','reqd',1);
		frm.set_df_property('location','reqd',1);
	}

	if(frappe.user.has_role("Customer")==1 && frappe.user!="Administrator"){
	    frm.remove_custom_button('Task','Create')
	    frm.remove_custom_button('Close')
	    frm.remove_custom_button('Cancel')
	    frm.remove_custom_button('Task','View')

	}


	},
	customer:function(frm){
		if (frm.doc.customer){
			frappe.db.get_value("Project",{'customer':frm.doc.customer},["name"], (val) => {
				if (val.name){
					frm.set_value("project",val.name);
				}
			})
	}
	if(frm.doc.customer){
		// frm.set_query('location', 'asset_details', function() {
		// 	if(frm.doc.customer){return {
		// 		query: 'mfi_customization.mfi.doctype.issue.get_location',
		// 		filters: {
		// 			"customer":frm.doc.customer
		// 		}
		// 	};}
		// });


		// frm.set_query('asset', 'asset_details', function() {
		// 	if(frm.doc.customer){return {
		// 		query: 'mfi_customization.mfi.doctype.issue.get_asset_on_cust',
		// 		filters: {
		// 			"customer":frm.doc.customer
		// 		}
		// 	};}
		// });
		// frm.set_query('serial_no', 'asset_details', function() {
		// 	if(frm.doc.customer){return {
		// 		query: 'mfi_customization.mfi.doctype.issue.get_asset_serial_on_cust',
		// 		filters: {
		// 			"customer":frm.doc.customer
		// 		}
		// 	};}
		// });
	}


	},

})

frappe.ui.form.on("Asset Readings", "type", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.type=='Black & White'){
	$("div[data-idx='"+d.idx+"']").find("input[data-fieldname='reading_2']").css('pointer-events','none')
    $("div[data-idx='"+d.idx+"']").find("input[data-fieldname='reading']").css('pointer-events','all')
	}
	if (d.type=="Colour"){
        $("div[data-idx='"+d.idx+"']").find("input[data-fieldname='reading_2']").css('pointer-events','all')
		$("div[data-idx='"+d.idx+"']").find("input[data-fieldname='reading']").css('pointer-events','none')
	}
	d.asset = frm.doc.asset
    refresh_field("asset", d.name, d.parentfield);
});

frappe.ui.form.on("Asset Readings", "date", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.idx>1){
        frappe.throw("More than one row not allowed")
    }
    d.asset = frm.doc.asset
    refresh_field("asset", d.name, d.parentfield);
});
// frappe.ui.form.on("Asset Details", "location", function(frm, cdt, cdn) {

//     var d = locals[cdt][cdn];
//     if(d.location){
//     frappe.db.get_value('Asset', {location: d.location,"docstatus":1}, ['asset_name','name','serial_no'], (r) => {
//         d.asset=r.name
//         d.serial_no=r.serial_no
//         d.asset_name = r.asset_name
//         refresh_field("asset", d.name, d.parentfield);
//         refresh_field("serial_no", d.name, d.parentfield);
//         refresh_field("asset_name",d.name, d.parentfield);
//        })
//     }

// });
// frappe.ui.form.on("Asset Details", "asset", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];
//     if(d.asset){
//         frappe.db.get_value('Asset', {name: d.asset,"docstatus":1}, ['location','serial_no'], (r) => {
//         d.location=r.location
//         d.serial_no=r.serial_no

//         refresh_field("location", d.name, d.parentfield);
//         refresh_field("serial_no", d.name, d.parentfield);
//        })
//     }
// });
// frappe.ui.form.on("Asset Readings", "type", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];
// 	if(d.type == 'Black & White'){
// 		frm.set_df_property("reading_2","read_only",1);
// 		frm.set_df_property("reading","read_only",0);
// 		console.log("in blk white");
// 	}
// 	if(d.type == 'Colour'){
// 		frm.set_df_property("reading","read_only",1);
// 		frm.set_df_property("reading_2","read_only",0);
// 		console.log("in colour");
// 	}
// 	if(d.type == 'Both'){
// 		frm.set_df_property("reading","read_only",0);

// 		frm.set_df_property("reading_2","read_only",0);

// 	}

// });



// frappe.ui.form.on("Asset Details", "serial_no", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];

//     if(d.serial_no){
//     frappe.db.get_value('Asset', {serial_no: d.serial_no,"docstatus":1}, ['location','name','asset_name'], (r) => {
//         d.asset_name=r.asset_name
//         d.location=r.location
//         d.asset=r.name
//         refresh_field("location", d.name, d.parentfield);
//         refresh_field("asset", d.name, d.parentfield);
//         refresh_field("asset_name", d.name, d.parentfield);
//        })
//       }
//     d.asset = frm.doc.asset
//     refresh_field("asset", d.name, d.parentfield);
// });


frappe.ui.form.on('Issue', {
    asset_name: function(frm) {
        if (frm.doc.item_code) {
            frappe.call({
                method: 'mfi_customization.mfi.doctype.issue.asset_name_item',
                args: {
                    item_code: frm.doc.item_code
                },
                callback: function(r) {
                    // frm.set_query("toner_type", function(doc) {
                    //     return {
                    //         "filters": [
                    //             ['Item', 'name', 'in', r.message]
                    //         ]
                    //     };
                    // });
		    frm.set_query('item','delivery_details',function(doc, cdt, cdn) {
			return {
                            "filters": [
                                ['Item', 'name', 'in', r.message]
                            ]
                        };
		    })

                }
            });
        }
    },
    refresh: function(frm) {
        if (frm.doc.item_code) {
            frappe.call({
                method: 'mfi_customization.mfi.doctype.issue.asset_name_item',
                args: {
                    item_code: frm.doc.item_code
                },
                callback: function(r) {
		     frm.set_query('item','delivery_details',function(doc, cdt, cdn) {
			return {
                            "filters": [
                                ['Item', 'name', 'in', r.message]
                            ]
                        };
		     })
                }
            });
        }
    }
});


// frappe.ui.form.on('Issue', {
//     asset: function(frm) {
//         if (!frm.doc.asset) {
//             frappe.call({
//                 method: 'mfi_customization.mfi.doctype.issue.user_customer',
//                 args: {
//                     user: frappe.session.user_email
//                 },
//                 callback: function(r) {

//                     if (r.message) {
//                         console.log(r.message[0]);
//                         frm.set_value("customer", r.message);
//                     }


//                 }
//             });
//         }
//     }
// });

function status_read_oly_fr_call_cordinator(frm){
         if((frappe.user.has_role("Call Coordinator") == 1 || frappe.user.has_role("Toner Coordinator") == 1)){
           frm.set_df_property('status',"read_only",1);
         }

}


function hide_request_mtrl_stus(frm){
     if((frappe.user.has_role("Call Coordinator") != 1 || frappe.user.has_role("Toner Coordinator") != 1)){
           frm.set_df_property('requested_material_status',"hidden",1);
     }
}

