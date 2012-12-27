var app = app || {};

(function() {
	'use strict';

	app.User = Backbone.Model.extend({

		/* id: unique
		 * name: string
		 */

		defaults: {
			name: ''
		}

	});

}());
