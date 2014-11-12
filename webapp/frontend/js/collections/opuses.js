var app = app || {};

(function() {
	'use strict';

	var OpusList = Backbone.Collection.extend({
		model: app.Opus,
		url: '/opuses'
	});

	app.Opus = new OpusList();

}());
