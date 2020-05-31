var chart = null; // 定义全局变量
var data = {};
$(document).ready(function () {
    $.get({
        url: '/get_data/',
        'success': function (point) {
            data = point;
        },
    });
    chart = chartfunc();
    chart.credits.update({
                text: 'Power by zhouluobo',
                href: 'https://www.luobodazahui.top/',
            });
    return data;
});