/*

=========================================================
* Volt - Bootstrap 5 Admin Dashboard
=========================================================

* Product Page: https://themesberg.com/product/admin-dashboard/volt-bootstrap-5-dashboard
* Copyright 2020 Themesberg (https://www.themesberg.com)

* Designed and coded by https://themesberg.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. Please contact us to request a removal.

*/

"use strict";
const d = document;
console.log("AAAA")
function ajaxFunctionGet(url){
    return fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(json => {
            return json
            }
        )
}

function test(url){
    fetch(url).then(function(response) {
        return response.json();
      })
}

async function fetchAsync (url) {
    let response = await fetch(url);
    let data = await response.json();
    return data;
  }

d.addEventListener("DOMContentLoaded", function(event) {

    // options
    const breakpoints = {
        sm: 540,
        md: 720,
        lg: 960,
        xl: 1140
    };

    var preloader = d.querySelector('.preloader');
    if(preloader) {
        setTimeout(function() {
            preloader.classList.add('show');

            setTimeout(function() {
                d.querySelector('.loader-element').classList.add('hide');
            }, 200);
        }, 1000);
    }

    var sidebar = document.getElementById('sidebarMenu')
    if(sidebar && d.body.clientWidth < breakpoints.lg) {
        sidebar.addEventListener('shown.bs.collapse', function () {
            document.querySelector('body').style.position = 'fixed';
        });
        sidebar.addEventListener('hidden.bs.collapse', function () {
            document.querySelector('body').style.position = 'relative';
        });
    }

    var iconNotifications = d.querySelector('.icon-notifications');
    if(iconNotifications) {
        var unreadNotifications = d.querySelector('.unread-notifications');
        var bellShake = d.querySelector('.bell-shake');
    
        if (iconNotifications.getAttribute('data-unread-notifications') === 'true') {
            unreadNotifications.style.display = 'block';
        } else {
            unreadNotifications.style.display = 'none';
        }
    
        // bell shake
        var shakingInterval = setInterval(function() {
            if (iconNotifications.getAttribute('data-unread-notifications') === 'true') {
                if (bellShake.classList.contains('shaking')) {
                    bellShake.classList.remove('shaking');
                } else {
                    bellShake.classList.add('shaking');
                }
            }
        }, 5000);
    
        iconNotifications.addEventListener('show.bs.dropdown', function () {
            bellShake.setAttribute('data-unread-notifications', false);
            clearInterval(shakingInterval);
            bellShake.classList.remove('shaking');
            unreadNotifications.style.display = 'none';
        });
    }

    [].slice.call(d.querySelectorAll('[data-background]')).map(function(el) {
        el.style.background = 'url(' + el.getAttribute('data-background') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-background-lg]')).map(function(el) {
        if(document.body.clientWidth > breakpoints.lg) {
            el.style.background = 'url(' + el.getAttribute('data-background-lg') + ')';
        }
    });

    [].slice.call(d.querySelectorAll('[data-background-color]')).map(function(el) {
        el.style.background = 'url(' + el.getAttribute('data-background-color') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-color]')).map(function(el) {
        el.style.color = 'url(' + el.getAttribute('data-color') + ')';
    });

    // Tooltips
    var tooltipTriggerList = [].slice.call(d.querySelectorAll('[data-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Popovers
    var popoverTriggerList = [].slice.call(d.querySelectorAll('[data-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
    })

    // Datepicker
    var datepickers = [].slice.call(d.querySelectorAll('[data-datepicker]'))
    var datepickersList = datepickers.map(function (el) {
        return new Datepicker(el, {
            buttonClass: 'btn'
          });
    })

    if(d.querySelector('.input-slider-container')) {
        [].slice.call(d.querySelectorAll('.input-slider-container')).map(function(el) {
            var slider = el.querySelector(':scope .input-slider');
            var sliderId = slider.getAttribute('id');
            var minValue = slider.getAttribute('data-range-value-min');
            var maxValue = slider.getAttribute('data-range-value-max');

            var sliderValue = el.querySelector(':scope .range-slider-value');
            var sliderValueId = sliderValue.getAttribute('id');
            var startValue = sliderValue.getAttribute('data-range-value-low');

            var c = d.getElementById(sliderId),
                id = d.getElementById(sliderValueId);

            noUiSlider.create(c, {
                start: [parseInt(startValue)],
                connect: [true, false],
                //step: 1000,
                range: {
                    'min': [parseInt(minValue)],
                    'max': [parseInt(maxValue)]
                }
            });
        });
    }

    if (d.getElementById('input-slider-range')) {
        var c = d.getElementById("input-slider-range"),
            low = d.getElementById("input-slider-range-value-low"),
            e = d.getElementById("input-slider-range-value-high"),
            f = [d, e];

        noUiSlider.create(c, {
            start: [parseInt(low.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
            connect: !0,
            tooltips: true,
            range: {
                min: parseInt(c.getAttribute('data-range-value-min')),
                max: parseInt(c.getAttribute('data-range-value-max'))
            }
        }), c.noUiSlider.on("update", function (a, b) {
            f[b].textContent = a[b]
        });
    }

    //Chartist

    if(d.querySelector('.ct-chart-sales-value')) {
        ajaxFunctionGet("/order_list/70/").then(function(data){
        //Chart 5
            var chart_data = Object.values(data)
            if (chart_data.length>1)
            {
                var percent = (chart_data[chart_data.length-1]-chart_data[chart_data.length-2])/chart_data[chart_data.length-2]*100
            }
            else{
                var percent = 0;
            }
            var percent_span = d.getElementById("orders-chart-percent");
            percent_span.innerHTML = percent + "%";
            new Chartist.Line('.ct-chart-sales-value', {
                labels: Object.keys(data),
                series: [
                    chart_data
                ]
            }, {
                low: 0,
                showArea: true,
                fullWidth: true,
                plugins: [
                Chartist.plugins.tooltip()
                ],
                axisX: {
                    // On the x-axis start means top and end means bottom
                    position: 'end',
                    showGrid: true
                },
                axisY: {
                    // On the y-axis start means left and end means right
                    showGrid: false,
                    showLabel: false,
                    labelInterpolationFnc: function(value) {
                        return '$' + (value / 1) + 'k';
                    }
                }
            });
        });
    }

    if(d.querySelector('.ct-chart-ranking')) {
        var chart = new Chartist.Bar('.ct-chart-ranking', {
            labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
            series: [
              [1, 5, 2, 5, 4, 3,100],
              [2, 3, 4, 8, 1, 2,20],
            ]
          }, {
            low: 0,
            showArea: true,
            plugins: [
              Chartist.plugins.tooltip()
            ],
            axisX: {
                // On the x-axis start means top and end means bottom
                position: 'end'
            },
            axisY: {
                // On the y-axis start means left and end means right
                showGrid: false,
                showLabel: false,
                offset: 0
            }
            });
          
          chart.on('draw', function(data) {
            if(data.type === 'line' || data.type === 'area') {
              data.element.animate({
                d: {
                  begin: 2000 * data.index,
                  dur: 2000,
                  from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
                  to: data.path.clone().stringify(),
                  easing: Chartist.Svg.Easing.easeOutQuint
                }
              });
            }
        });
    }

    if(d.querySelector('.ct-chart-traffic-share')) {
        console.log("!!!!!!!")
        var test_data = {
            series: [70, 20, 10]
          };
          var sum = function(a, b) { return a + b };
          
          new Chartist.Pie('.ct-chart-traffic-share', test_data, {
            labelInterpolationFnc: function(value) {
              return Math.round(value / test_data.series.reduce(sum) * 100) + '%';
            },            
            low: 0,
            high: 8,
            donut: true,
            donutWidth: 20,
            donutSolid: true,
            fullWidth: false,
            showLabel: false,
            plugins: [
              Chartist.plugins.tooltip()
            ],
        });
        console.log("!!!!")
        ajaxFunctionGet("/searchInfo/").then(function(data){
            console.log("1111111")
            console.log(data);
            var search_data_good = {
                series: data.good
            }
            var search_data_bad = {
                series: data.bad
            }
            new Chartist.Pie('#good_search', search_data_good, {            
                low: 0,
                high: 8,
                donut: true,
                donutWidth: 20,
                donutSolid: true,
                fullWidth: false,
                showLabel: true,
                plugins: [
                Chartist.plugins.tooltip()
                ],
            }); 
            new Chartist.Pie('#bad_search', search_data_bad, {            
                low: 0,
                high: 8,
                donut: true,
                donutWidth: 20,
                donutSolid: true,
                fullWidth: false,
                showLabel: true,
                plugins: [
                Chartist.plugins.tooltip()
                ],
            });     
        });
    }

    if (d.getElementById('loadOnClick')) {
        d.getElementById('loadOnClick').addEventListener('click', function () {
            var button = this;
            var loadContent = d.getElementById('extraContent');
            var allLoaded = d.getElementById('allLoadedText');
    
            button.classList.add('btn-loading');
            button.setAttribute('disabled', 'true');
    
            setTimeout(function () {
                loadContent.style.display = 'block';
                button.style.display = 'none';
                allLoaded.style.display = 'block';
            }, 1500);
        });
    }

    var scroll = new SmoothScroll('a[href*="#"]', {
        speed: 500,
        speedAsDuration: true
    });

    if(d.querySelector('.current-year')){
        d.querySelector('.current-year').textContent = new Date().getFullYear();
    }

});