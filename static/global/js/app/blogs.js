/* Models */

App.News = DS.Model.extend({
    url: 'blogs/news',
    slug: DS.attr('string'),
    title: DS.attr('string'),
    body: DS.attr('string'),
    publicationDate: DS.attr('date'),
    author: DS.belongsTo('App.UserPreview')
});

App.NewsPreview = DS.Model.extend({
    url: 'blogs/preview/news',
    slug: DS.attr('string'),
    title: DS.attr('string'),
    publicationDate: DS.attr('date')
});

/* Controller */


/* Views */

App.NewsItemView = Em.View.extend({
    templateName: 'news_item'
});

App.NewsIndexView = Em.View.extend({
    templateName: 'news_index'
});


App.NewsItemPreviewView = Em.View.extend({
    templateName: 'news_item_preview'
});

App.NewsView = Em.View.extend({
    templateName: 'news'
});

