var app = app || {};

(function() {
	'use strict';

	var OpusList = Backbone.Collection.extend({

		model: app.Opus,

		localStorage: new Store('opuses'),

		byUser: function(id) {
			return this.filter({user: id});
		},
	
		byAuthor: function(id) {
			return this.filter({author: id});
		}

	});

	app.Opus = new OpusList();

}());
