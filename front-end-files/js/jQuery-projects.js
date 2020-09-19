$.each([0, 4, 8, 12], (_, n) => {
  $('.overlay').eq(n).css("backgroundColor", "var(--red");;
  $('.card-body').eq(n).css("color", "var(--red");
});


$.each([1, 5, 9], (_, n) => {
  $('.overlay').eq(n).css("backgroundColor", "var(--orange");;
  $('.card-body').eq(n).css("color", "var(--orange");
});

$.each([2, 6, 10], (_, n) => {
  $('.overlay').eq(n).css("backgroundColor", "var(--yellow");;
  $('.card-body').eq(n).css("color", "var(--yellow");
});

$.each([3, 7, 11], (_, n) => {
  $('.overlay').eq(n).css("backgroundColor", "var(--green");;
  $('.card-body').eq(n).css("color", "var(--green");
});