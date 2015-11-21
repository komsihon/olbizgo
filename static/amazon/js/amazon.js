/**
 * Created by Kom Sihon on 11/18/15.
 */
(function(c) {
    c.listItemsHome = function(endpoint, category, start, length) {
        var $newSection = $('div#content section.tpl').clone().removeClass('tpl'),
            params = {format: 'json', category_id: category.id, start: start, length: length};
        $newSection.insertBefore('section.tpl').addClass(category.slug + ' ' + category.items_size + '-items')
            .show().find('header span').text(category.title);
        $newSection.find('header a').attr('href', '/boutique/' + category.slug);
        $.getJSON(endpoint, params, function(data) {
            var $targetSection = $('div#content section.' + category.slug);
            $targetSection.find('.spinner').remove();
            if (data.error) {
                $('div#top-notice-ctnr span').html(data.error).addClass('failure');
                $('#top-notice-ctnr').fadeIn().delay(6000).fadeOut();
                return;
            }
            var $list = $('<div></div>');
            for (var i = 0; i < data.length; i++) {
                var $item = $targetSection.find('.item.tpl').clone().removeClass('tpl');
                $item = applyItemTemplate($item, data[i]).show();
                $list.append($item)
            }
            $targetSection.find('.item.tpl').before($list.children())
        })
    };
    c.listItems = function(endpoint, categoryId, start, length) {
        var params = {format: 'json', category_id: categoryId, start: start, length: length};
        $('div#items section .spinner').show();
        $.getJSON(endpoint, params, function(data) {
            $('div#items section .spinner').hide();
            if (data.error) {
                $('div#top-notice-ctnr span').html(data.error).addClass('failure');
                $('#top-notice-ctnr').fadeIn().delay(6000).fadeOut();
                return;
            }
            if (data.length == 0) {
                if ($('div#items section .item:not(.tpl)').length == 0) {
                    var $emptyResult = $('<div class="no-result">Aucune donnée trouvée</div>');
                    $emptyResult.insertBefore('div#items section .spinner');
                    return
                }
                ikwen.dataSourceEmpty = true
            }
            var $list = $('<div></div>');
            for (var i = 0; i < data.length; i++) {
                var $item = $('div#items section .item.tpl').clone().removeClass('tpl');
                $item = applyItemTemplate($item, data[i]).show();
                $list.append($item)
            }
            $('div#items section .item.tpl').before($list.children())
        })
    };
    function applyItemTemplate($tplItem, item) {
        $tplItem.find('a.button').attr('href', item.href).text(item.button_text).addClass(item.button_style);
        $tplItem.find('span.title span:first').text(item.title);
        $tplItem.prepend($(item.embed_code));
        $tplItem.find('a:first-child').attr('title', item.title);
        return $tplItem
    }
})(ikwen);