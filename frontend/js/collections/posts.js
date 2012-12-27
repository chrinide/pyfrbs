var app = app || {};

(function() {
	'use strict';

	var PostList = Backbone.Collection.extend({

		model: app.Post,

		localStorage: new Store('posts'),

		byUser: function(id) {
			return this.where({user: id});
		},

		comparator: function(post) {
			return post.get('date');
		}

	});

	app.Posts = new PostList();

}());
