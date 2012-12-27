var app = app || {};

(function() {
	'use strict';

	var UserList = Backbone.Collection.extend({

		model: app.User,

		localStorage: new Store('users')

	});

	app.Users = new UserList();

}());
