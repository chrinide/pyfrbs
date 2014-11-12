var app = app || {};

(function() {
	'use strict';

	var Workspace = Backbone.Router.extend({
		routes:{
			'*filter': 'setFilter'
		},

		setFilter: function( param ) {
			app.PostFilter = param.trim() || '';

			app.Posts.trigger('filter');
		}
	});

	app.PostRouter = new Workspace();
	Backbone.history.start();

}());
