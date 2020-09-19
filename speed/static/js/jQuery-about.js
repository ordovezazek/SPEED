var pages = [ '#about', '#histo', '#vm', '#comp', '#values', '#awards' ];
var pagesArrowDown = ['#about', '#histo', '#vm', '#comp', '#values', '#awards'];

$('#navbar-about a').click(function (e) {
  var targetHref = $(this).attr('href');

  $('html, body').animate({
    scrollTop: $(targetHref).offset().top - $('.navbar-expand-xl').height()
  }, 1000);

  e.preventDefault();
});

function goTo (selector) {
  var offset = $(selector).height() + $(collapsibleNavbar).height();
  if (selector === 'about') {
    navigate('about-nav');
  }
  $('html,body').animate({ scrollTop: $(selector).offset().top - $('.navbar-expand-xl').height()}, 1000);
};

function navigate(nav, text) {
  if (!$(nav).hasClass('active')) {
    remove(nav);
    $(nav).addClass('active');
    $(text).fadeIn(180);
    $(text).removeClass('inactive');
  }
};

function remove(cl) {
  pages.forEach(function(page) {
    if (cl !== page + '-nav') {
      $(page + '-nav').removeClass('active');
      $(page + '-text').fadeOut(0);
    }
  });
}

function isVisible($el) {
  var winTop = $(window).scrollTop();
  var winBottom = winTop + $(window).height();
  var elTop = $el.offset().top;
  var elBottom = elTop + $el.height();
  return (elBottom - winTop >= $el.height()/2) && (elBottom - winTop <= $el.height() * elBottom/$el.height());
}

$(function() {
  $(window).scroll(function() {
    if (isVisible($("#about")) ) {
      navigate('#about-nav', '#about-text');
    } else if (isVisible($("#histo")) ) {
      navigate('#histo-nav', '#histo-text');
    } else if (isVisible($("#vm")) ) {
      navigate('#vm-nav', '#vm-text');
    } else if (isVisible($("#comp")) ) {
      navigate('#comp-nav', '#comp-text');
    } else if (isVisible($("#values")) ) {
      navigate('#values-nav', '#values-text');
    } else if (isVisible($("#awards"))) {
      navigate('#awards-nav', '#awards-text');
    }
  });
});