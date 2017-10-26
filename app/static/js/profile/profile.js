var model_id=1;

var AwardCollection = Backbone.Collection.extend({
	url: '/profile/display_award'
});

var awardCollection = new AwardCollection();
awardCollection.fetch();

var awardModel = new Backbone.Model();

var awardmodelfunction = function(){
	var new_model = awardCollection.get(model_id);
	awardModel.set(new_model.toJSON());
}


var show_mainview = function(){
	var award_length = awardCollection.length;
	if (model_id <award_length){
		setTimeout(function() {
			model_id+=1;
			awardmodelfunction();
        }, 3000);
	}
	else if(model_id>=award_length){
		setTimeout(function() {
			$('.award_popup').hide();
			 $.ajax({
    			method:'POST',
    			url:'/profile/reset_display'
    		});
		}, 3000);
	}
}

var MainView = Mn.View.extend({
	tagname:'div',
	model: awardModel,
	template:_.template($('#award_view').html()),

	initialize: function(){
		this.listenTo(this.model, 'change', this.render);
	},

	onRender(){
		show_mainview();
	}
});

var mainView = new MainView();

var award = new Marionette.Application({
	region:'.award_popup'
});



awardCollection.on("sync", function(){
	try{
		awardmodelfunction();
	}
	catch(err) {
		$('.award_popup').hide();
	}

	award.showView(mainView);
});
