var app = app || {};

(function() {
	'use strict';

	var PostList = Backbone.Collection.extend({
		model: app.Post,
		url: '/posts'
	});

	app.Posts = new PostList();

}());
