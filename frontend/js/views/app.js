var app = app || {};

$(function( $ ) {
	'use strict';

	app.AppView = Backbone.View.extend({

		el: '#43app',

		events: {
			'keypress #new-post': 'createOnEnter',
		},

		initialize: function() {
			this.input = this.$('#new-post');
			this.$main = this.$('#main');

			app.Posts.on( 'add', this.addOne, this );
			app.Posts.on( 'reset', this.addAll, this );
			app.Posts.on( 'filter', this.filterAll, this );
			app.Posts.on( 'all', this.render, this );

			app.Posts.fetch();
		},

		render: function() {
			if ( app.Posts.length ) {
				this.$main.show();
			} else {
				this.$main.hide();
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

		newAttributes: function() {
			return {
				summary: this.input.val().trim()
			};
		},

		createOnEnter: function( e ) {
			if ( e.which !== ENTER_KEY || !this.input.val().trim() ) {
				return;
			}

			app.Posts.create( this.newAttributes() );
			this.input.val('');
		}

	});
});
