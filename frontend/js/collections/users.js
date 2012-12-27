var app = app || {};

(function() {
	'use strict';

	var UserList = Backbone.Collection.extend({
		model: app.User,
		url: '/users'
	});

	app.Users = new UserList();

}());
