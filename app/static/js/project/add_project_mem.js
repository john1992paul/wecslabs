
var Members = Backbone.Collection.extend({
	url: '/create_project/add_project_mem/fetch_users'
});

var members = new Members();
members.fetch({reset:true});

var ProjectMembers = Backbone.Collection.extend({});

var projectMembers = new ProjectMembers([]);

var MemberItemView = Mn.View.extend({
	tagname: 'div',
	className: 'member',
	template: _.template($('#member_view').html()),

	triggers: {
		'click #add_button': 'select:add'
	}
}); 

var MembersView = Mn.CollectionView.extend({
	tagname: 'div',
	childView: MemberItemView,
	collection: members,
	childViewEvents: {
		'select:add': 'addSelected'
	},

	addSelected: function(childView){
		mods = childView.model;
		projectMembers.add([mods]);
		if (projectMembers.length == 1) {
			$('#submit_btn').toggleClass('hidden');
		}
	}
});

var ProjectMemberItemView = Mn.View.extend({
	tagname: 'div',
	className: 'member',
	template: _.template($('#project_member_view').html()),

	triggers: {
		'click #delete_button': 'select:delete',
		'dblclick #position': 'select:display',
		'keyup #role': 'select:role'
	}
}); 

var ProjectMembersView = Mn.CollectionView.extend({
	tagname: 'div',
	childView: ProjectMemberItemView,
	collection: projectMembers,
	childViewEvents: {
		'select:delete': 'deleteSelected',
		'select:display': 'display_edit',
		'select:role': 'updateonenter'
	},

	deleteSelected: function(childView){
		mods = childView.model;
		projectMembers.remove(mods);
		if (projectMembers.length == 0) {
			$('#submit_btn').toggleClass('hidden');
		}
	},
	display_edit: function(childView, e){
		$(e.currentTarget).parent().children('.role').toggleClass('hidden');
	},
	updateonenter: function(childView, e){

		if (e.which==13) {
			mods = childView.model;
			mods.set({'position': $(e.currentTarget).val()});
			projectMembersView.render();
		}
	}
});

$("#submit_btn").click(function(){
	var data = {'info':JSON.stringify(projectMembers.toJSON()),'project_name': $('#project_name').text()};
	console.log(data);
    $.ajax({
    	method:'POST',
    	url:'/create_project/add_project_mem/submit',
    	data: data,
    	success: function(result) {
    		url = '/project_activities/' + $('#project_name').text();
    		setTimeout(function() {
                window.location.href = url;
            }, 500);
    	}
    })
});

var projectMembersView = new ProjectMembersView();

var MainView = Mn.View.extend({
	tagname:'div',
	template:_.template($('#main_view').html()),

	regions: {
		members:'#subcontainer_members',
		projectMembers: '#subcontainer_main'

	},

	onRender() {
		this.showChildView('members', new MembersView());
		this.showChildView('projectMembers', projectMembersView);
	}
});

var mainView = new MainView();

var projectPlanner = new Marionette.Application({
	region:'#main_container'
});

members.on("sync", function(){
	projectPlanner.showView(mainView);
});