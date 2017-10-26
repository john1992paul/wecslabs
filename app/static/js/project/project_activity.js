$(document).ready(function(){

var toggler_status = 0;
var activities_added = 0;

var url = ''

var ActivityDate = Backbone.Model.extend({
	url: '/project_activities/fetch_current_date'
});

var activityDate = new ActivityDate();
activityDate.fetch();

var Activities = Backbone.Collection.extend({
	url: function(){
		return url
	}
});

var activities = new Activities();


activityDate.on("sync", function(){
	var current_date = activityDate.toJSON()['date'];
	var stripped_date = current_date.replace("/", "").replace("/", "");
	url = '/project_activities/fetch_activities/' + stripped_date + '/' + $('#project_global_name').text();
	activities.fetch();
});

var today = new Activities();

var update_today = function(date){
	var current_date = activityDate.toJSON()['date'];
	var grouped = activities.groupBy('date');
	var today_temp = (new Backbone.Collection(grouped[current_date])).toJSON();
	today.reset();
	today.add(today_temp);
}


var ActivityItemView = Mn.View.extend({
	tagname: 'div',
	className: 'activity_container',
	template: _.template($('#activity_template').html()),

	triggers: {
		'click #check': 'select:check',
		'click #delete': 'select:delete'
	}
}); 

var ActivitiesView = Mn.CollectionView.extend({
	tagname: 'div',
	childView: ActivityItemView,
	collection: update_today,

	initialize: function(){
		this.listenTo(this.collection, 'change', this.render);
		this.listenTo(this.collection, 'destroy', this.destroy);
	},

	childViewEvents: {
		'select:check': 'checkToggler',
		'select:delete': 'deleteActivity'
	},

	checkToggler: function(childView){
		mods = childView.model;
		if(mods.toJSON()['checked'] == 1){
			activity = mods.toJSON()['activity_name'];
			var x =activities.find(function(model) { return model.get('activity_name') === activity; });
			mods.set({'checked': 0});
			x.set({'checked': 0});
			toggler_status-=1;

			console.log(toggler_status);
			$('.hide_arrow').toggleClass('hide_arrow');
		}
		else if(mods.toJSON()['checked'] == 0) {
			activity = mods.toJSON()['activity_name'];
			var x =activities.find(function(model) { return model.get('activity_name') === activity; });
			mods.set({'checked': 1});
			x.set({'checked': 1});
			toggler_status+=1;
			console.log(toggler_status);
			$('.hide_arrow').toggleClass('hide_arrow');
		}
	},

	deleteActivity: function(childView){
		activities_added -= 1;
		console.log(activities_added);
		mods = childView.model;
		activity = mods.toJSON()['activity_name'];
		var x =activities.find(function(model) { return model.get('activity_name') === activity; });
		activities.remove(x);
		today.remove(mods);
		$('.hide_arrow').toggleClass('hide_arrow');
	}
});


var activitiesView = new ActivitiesView();


var HeaderView = Mn.View.extend({
	tagname:'div',
	className:'activity_day',
	model:activityDate,
	template:_.template($('#date_header_template').html()),

	initialize: function(){
		this.listenTo(this.model, 'change', this.render);
	},

	events: {
		'click #toggle_button': 'hide_unhide',
		'click #add_button': 'add_activity',
		'keyup #input_activity': 'add_new_activity',
		'click #next_day': 'next_day',
		'click #previous_day': 'previous_day',
		'click #save_button': 'save_activities'
	},

	hide_unhide: function(){
		$('#activities_list').toggleClass('hidden');
		if($('#toggle_button img').attr('src') == "/static/img/project/down.png"){
			$('#toggle_button img').attr('src','/static/img/project/right.png');
		}
		else {
			$('#toggle_button img').attr('src','/static/img/project/down.png');
		}
	},

	add_activity: function(){
		$('#add_new').toggleClass('hidden');
	},

	add_new_activity: function(e){
		if(e.which == 13){
			activities_added+=1;
			console.log(activities_added);
			var activity_name = $('#input_activity').val();
			var date = $('#date').text();
			var checked = 0;
			activities.add([{'activity_name':activity_name, 'checked':checked, 'date': date}]);
			$('#input_activity').val('');
			update_today(date);
			$('.hide_arrow').toggleClass('hide_arrow');
		}
		else if(e.which == 27){
			$('#input_activity').val('');
		}
	},

	next_day: function(){
		activities_added = 0;
		var current_date = activityDate.toJSON()['date'];
		var current_date = new Date(current_date);
		current_date.setDate(current_date.getDate() + 1);
		var next_date = String((current_date.getMonth() + 1) +'/' + current_date.getDate() +'/' + current_date.getFullYear());
		var stripped_date = next_date.replace("/", "").replace("/", "");
		url = '/project_activities/fetch_activities/' + stripped_date+ '/' + $('#project_global_name').text();
		activities.fetch();
		activities.on("sync", function(){
			activityDate.set({'date':next_date});
			update_today();
		});
	},

	previous_day: function(){
		activities_added = 0;
		toggler_status = 0;
		var current_date = activityDate.toJSON()['date'];
		var current_date = new Date(current_date);
		current_date.setDate(current_date.getDate() - 1);
		var previous_date = String((current_date.getMonth() + 1) +'/' + current_date.getDate() +'/' + current_date.getFullYear());
		var stripped_date = previous_date.replace("/", "").replace("/", "");
		url = '/project_activities/fetch_activities/' + stripped_date+ '/' + $('#project_global_name').text();
		activities.fetch();
		activities.on("sync", function(){
			activityDate.set({'date':previous_date});
			update_today();
		});
	},

	save_activities: function(){
		var current_date = activityDate.toJSON()['date'];
		var grouped = activities.groupBy('date');
		var today_temp = (new Backbone.Collection(grouped[current_date])).toJSON();
		console.log(activities_added);
		var activity_upload = {'info':JSON.stringify(today_temp),'project_name':$('#project_name').text(),'date':current_date, 'toggler_status': toggler_status, 'activities_added': activities_added};
		$.ajax({
    		method:'POST',
    		url:'/project_activities/save_activities',
    		data: activity_upload
    	});
    	activities_added = 0;
		toggler_status = 0;
    	$('.save_arrow').toggleClass('hide_arrow');
	}
});

var headerView = new HeaderView();

var MainView = Mn.View.extend({
	tagname:'div',
	template:_.template($('#main_template').html()),

	regions: {
		activity_regions:'#activity_regions',
		activities_list:'#activities_list'
	},

	onRender() {
		var current_date = activityDate.toJSON()['date'];
		var grouped = activities.groupBy('date');
		today = new Backbone.Collection(grouped[current_date]);
		this.showChildView('activity_regions', headerView);
		this.showChildView('activities_list', new ActivitiesView({collection: today}));
	}
});

var mainView = new MainView();

var activityPlanner = new Marionette.Application({
	region:'#main_container'
});

activities.on("sync", function(){
	activityPlanner.showView(mainView);
});

});