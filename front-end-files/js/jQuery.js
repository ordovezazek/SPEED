$(function () {
  $(document).scroll(function () {
    var $nav = $(".fixed-top");
    $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
  });
});

//edited lines 1235 & 1238 to change navbar toggler icon when active
  $('#nav-vm').click(function () {
    $('html, body').animate({
      scrollTop: $("#row-vm").offset().top - $('.navbar-expand-xl').height()
    }, 1000)
  });

  