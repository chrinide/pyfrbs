var app = app || {};

(function() {
	'use strict';

	var AuthorList = Backbone.Collection.extend({

		model: app.Author,

		localStorage: new Store('authors'),

		original: function(id) {
			return this.get(this.get(id).at(0).original);
		},

		aliases: function(id) {
			return this.where({original: this.original(id)});
		}

	});

	app.Authors = new AuthorList();

}());
