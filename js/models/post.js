var app = app || {};

(function() {
	'use strict';

	app.Post = Backbone.Model.extend({

		/* id: unique
		 * user: User.id
		 * date: string
		 * opus: Opus.id
		 * tags: string
		 * summary: string
		 */

		defaults: {
			tags: '',
			summary: ''
		}

	});

}());
