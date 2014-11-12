var app = app || {};

$(function( $ ) {
	'use strict';

	app.AppView = Backbone.View.extend({

		el: '#app-section',

		events: {
			'click #new-post': 'create'
		},

		initialize: function() {
			app.Posts.on('add', this.addOne, this);
			app.Posts.on('reset', this.addAll, this);
			app.Posts.on('filter', this.filterAll, this);
			app.Posts.on('all', this.render, this);
			app.Posts.fetch();
		},

		render: function() {
			if (app.Posts.length) {
				this.$('#main-section').show();
			} else {
				this.$('#main-section').hide();
			}
		},

		addOne: function( post ) {
			var view = new app.PostView({ model: post });
			$('#post-list').append( view.render().el );
		},

		addAll: function() {
			this.$('#post-list').html('');
			app.Posts.each(this.addOne, this);
		},

		filterOne : function (post) {
			post.trigger('visible');
		},

		filterAll : function () {
			app.Posts.each(this.filterOne, this);
		},

		create: function() {
			app.Posts.create({ 
				opus: this.$('#new-post-opus').val().trim(),
				summary: this.$('#new-post-summary').val().trim(),
				tags: this.$('#new-post-tags').val().trim()
			});
		}

	});
});
