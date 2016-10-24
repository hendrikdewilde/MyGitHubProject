//copyright 2008 Jarrett Vance
//http://jvance.com
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

$.fn.rater = function(options) {
    var opts = $.extend({}, $.fn.rater.defaults, options);
    return this.each(function() {
        var $this = $(this);
        var $on = $this.find('.ui-rater-starsOn');
        var $off = $this.find('.ui-rater-starsOff');
        opts.size = $on.height();
        if (opts.rating == undefined) opts.rating = $on.width() / opts.size;
        if (opts.id == undefined) opts.id = $this.attr('id');

        $off.mousemove(function(e) {
            var left = e.clientX - $off.offset().left;
            var width = $off.width() - ($off.width() - left);
            width = Math.ceil(width / (opts.size / opts.step)) * opts.size / opts.step;
            $on.width(width);
        }).hover(function(e) { $on.addClass('ui-rater-starsHover'); }, function(e) {
            $on.removeClass('ui-rater-starsHover'); $on.width(opts.rating * opts.size);
        }).click(function(e) {
            var r = Math.round($on.width() / $off.width() * (opts.units * opts.step)) / opts.step;
            $off.unbind('click').unbind('mousemove').unbind('mouseenter').unbind('mouseleave');
            $off.css('cursor', 'default'); $on.css('cursor', 'default');
            $.fn.rater.rate($this, opts, r);
        }).css('cursor', 'pointer'); $on.css('cursor', 'pointer');
    });
};

$.fn.rater.defaults = {
    postHref: location.href,
    units: 5,
    step: 1
};

$.fn.rater.rate = function($this, opts, rating) {
    var $on = $this.find('.ui-rater-starsOn');
    var $off = $this.find('.ui-rater-starsOff');
    $off.fadeTo(600, 0.4, function() {
        $.ajax({
            url: opts.postHref,
            type: "POST",
            data: 'id=' + opts.id + '&rating=' + rating,
            complete: function(req) {
                if (req.status == 200) { //success
                    opts.rating = parseFloat(req.responseText);
                    $off.fadeTo(600, 0.1, function() {
                        $on.removeClass('ui-rater-starsHover').width(opts.rating * opts.size);
                        var $count = $this.find('.ui-rater-rateCount');
                        $count.text(parseInt($count.text()) + 1);
                        $this.find('.ui-rater-rating').text(opts.rating.toFixed(1));
                        $off.fadeTo(600, 1);
                        $this.attr('title', 'Your rating: ' + rating.toFixed(1));
                    });
                } else { //failure
                    alert(req.responseText);
                    $on.removeClass('ui-rater-starsHover').width(opts.rating * opts.size);
                    $this.rater(opts);
                    $off.fadeTo(2200, 1);
                }
            }
        });
    });
};
