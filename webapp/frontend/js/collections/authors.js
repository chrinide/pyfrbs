var app = app || {};

(function() {
	'use strict';

	var AuthorList = Backbone.Collection.extend({
		model: app.Author,
		url: '/authors'
	});

	app.Authors = new AuthorList();

}());
