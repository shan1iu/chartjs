function ajaxDataPubSummary(url, f) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            f(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function ajaxDataPubBy(url, f, type, canvas_id) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            f(response, type, canvas_id);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function ajaxDataAverages(url, canvas_id, f, data_id) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            f(response["data"], canvas_id, data_id);
        },
        error: function (error) {
            console.log(error);
        }
    });
}
function ajaxDataCoauthor(url, f, canvas_id) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            f(response["data"], canvas_id);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

//labels dataset label text
function plotPubSummary(data) {
    $("#canvas_id").css("display", "block");
    $('#bar-chart-grouped').css("display", "block");
    $("#bar-chart-grouped5").css("display", "none");
    var id_ctx = document.getElementById("bar-chart-grouped");
    var ctx = id_ctx.getContext('2d');
    var myChart = new Chart(document.getElementById("bar-chart-grouped"), {
        type: 'horizontalBar',
        data: {
            labels: data["data"][0].slice(1),
            datasets: [
                {
                    label: data["data"][0].slice(1)[0],
                    backgroundColor: "rgba(76, 175, 80, 0.4)",
                    borderColor: "rgba(76, 175, 80, 1)",
                    borderWidth: 1,
                    data: data["data"][1][0].slice(1)
                }, {
                    label: data["data"][0].slice(1)[1],
                    backgroundColor: "rgba(238, 110, 115, 0.4)",
                    borderColor: "rgba(238, 110, 115, 1)",
                    borderWidth: 1,
                    data: data["data"][1][1].slice(1)
                }
            ]
        },
        options: {
            title: {
                display: true,
                text: 'Publication Summary',
                fontSize: "25"
            },
            scales: {
                xAxes: [{ticks: {fontSize: 15}}],
                yAxes: [{ticks: {fontSize: 15}}]
            }
        }
    });
}


function showPlot(button_id, canvas_id) {
    $("#" + button_id).attr('disabled', 'disabled').parent().siblings().children().removeAttr('disabled');
    $("#" + canvas_id).show().siblings().hide();
}

function plotPubByAuthor(data, type, canvas_id) {
    $("#type_id").css("display", "block");
    $("#canvas_id").css("display", "block");
    //$("#" + canvas_id).siblings().hide();
    //label types : ["Number of conference papers", "Number of journals", "Number of books", "Number of book chapters", "Total"]
    var author = [];
    var lengthOfData = data["data"][1].length;
    var dataOfType = []; // store data for different type
    for (var i = 0; i < lengthOfData; i++) {
        author.push(data["data"][1][i][0]);
    }
    // get data for different type :
    if (type === "1") { // "Number of conference papers" // data["data"][1][*][1]
        label = "Number of Conference Papers";
        for (var j = 0; j < lengthOfData; j++) {
            if (data["data"][1][j][1] !== 0) {
                var authorName = author[j];
                var authorData = data["data"][1][j][1];
                dataOfType.push({author: authorName, data: authorData});
            }
        }
    } else if (type === "2") { // "Number of journals" // data["data"][1][*][2]
        label = "Number of Journals";
        for (var k = 0; k < lengthOfData; k++) {
            if (data["data"][1][k][2] !== 0) {
                var authorName1 = author[k];
                var authorData1 = data["data"][1][k][2];
                dataOfType.push({author: authorName1, data: authorData1});
            }
        }
    } else if (type === "3") { // "Number of books" // data["data"][1][*][3]
        label = "Number of Books";
        for (var l = 0; l < lengthOfData; l++) {
            if (data["data"][1][l][3] !== 0) {
                var authorName2 = author[l];
                var authorData2 = data["data"][1][l][3];
                dataOfType.push({author: authorName2, data: authorData2});
            }
        }
    } else if (type === "4") { // "Number of book chapters" // data["data"][1][*][4]
        label = "Number of Book Chapters";
        for (var m = 0; m < lengthOfData; m++) {
            if (data["data"][1][m][4] !== 0) {
                var authorName3 = author[m];
                var authorData3 = data["data"][1][m][4];
                dataOfType.push({author: authorName3, data: authorData3});
            }
        }
    } else if (type === "5") { // "Total" // data["data"][1][*][5]
        label = "Total";
        for (var o = 0; o < lengthOfData; o++) {
            if (data["data"][1][o][1] !== 0) {
                var authorName4 = author[o];
                var authorData4 = data["data"][1][o][5];
                dataOfType.push({author: authorName4, data: authorData4});
            }
        }
    }
    dataOfType.sort(function (a, b) {
        if (a["data"] > b["data"]) {
            return -1;
        } else if (a["data"] < b["data"]) {
            return 1;
        } else {
            return 0;
        }
    });

    var dataForPlot_name = [];
    var dataForPlot_data = [];
    var dataForPlot_bg_color = [];
    var bg_color_list = [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)'
    ];
    for (var p = 0; p < dataOfType.length; p++) {
        dataForPlot_name.push(dataOfType[p]["author"]);
        dataForPlot_data.push(dataOfType[p]["data"]);
        dataForPlot_bg_color.push(bg_color_list[Math.floor(Math.random() * bg_color_list.length)]);
    }
    var lengthOfCanvas = 0;
    if (dataOfType.length < 300) {
        lengthOfCanvas = dataOfType.length * 12;
    } else {
        lengthOfCanvas = dataOfType.length * 6;
    }

    $("#" + canvas_id).attr("height", lengthOfCanvas);
    var ctx = document.getElementById(canvas_id).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: dataForPlot_name,
            datasets: [
                {
                    label: label,
                    backgroundColor: dataForPlot_bg_color,
                    data: dataForPlot_data
                }
            ]
        },
        options: {
            legend: {display: false},
            title: {
                display: false,
                text: label,
                fontSize: 20
            },
            scales: {
                xAxes: [{
                    ticks: {
                        fontSize: 13,
                        beginAtZero: true
                    }
                }],
                yAxes: [{ticks: {fontSize: 13}}]
            },
            tooltips: {
                enabled: true
            }
        }
    });
}

function plotPubAverages(data, canvas_id, data_id) {
    console.log("data : ", data[data_id], "canvas_id : ", canvas_id);
    var text = data[data_id]["title"];
    var labels = data[data_id]["header"].slice(1);
    //console.log(data[data_id]["rows"][0].slice(1));
    //console.log(data[data_id]["rows"][1].slice(1));
    var ctx = document.getElementById(canvas_id).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Mean",
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)'],
                    data: data[data_id]["rows"][0].slice(1)
                },
                {
                    label: "Medium",
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(56, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(123, 107, 255, 0.7)'],
                    data: data[data_id]["rows"][1].slice(1)
                }
            ]
        },
        options: {
            title: {
                display: true,
                text: text,
                fontSize: 17
            },
            tooltips: {
                enabled: true
            },
            scaleLabel: {
                display: true
            }
        }
    });
}

function randomColor() {
    var color_list = [
        {
            backgroundColor: "rgba(255,221,50,0.2)",
            borderColor: "rgba(255,221,50,1)"
        },
        "rgb(244, 67, 54, 0.7)",
        "rgb(33, 150, 243, 0.7)",
        "rgb(76, 175, 80, 0.7)",
        "rgb(255, 235, 59, 0.7)",
        "rgb(158, 158, 158, 0.7)",
        "rgb(103, 58, 183, 0.7)"
    ];
    return color_list[Math.floor(Math.random() * color_list.length)]
}

function bg_bd_color() {
    var color_bd_bg_list = [
        {
            backgroundColor: "rgb(244, 67, 54, 0.3)",
            borderColor: "rgb(244, 67, 54, 1)"
        },
        {
            backgroundColor: "rgb(33, 150, 243, 0.3)",
            borderColor: "rgb(33, 150, 243, 1)"
        },
        {
            backgroundColor: "rgb(76, 175, 80, 0.3)",
            borderColor: "rgb(76, 175, 80, 1)"
        },
        {
            backgroundColor: "rgb(255, 235, 59, 0.3)",
            borderColor: "rgb(255, 235, 59, 1)"
        },
        {
            backgroundColor: "rgb(158, 158, 158, 0.2)",
            borderColor: "rgb(158, 158, 158, 1)"
        },
        {
            backgroundColor: "rgb(103, 58, 183, 0.3)",
            borderColor: "rgb(103, 58, 183, 0.7)"
        }
    ];
    return color_bd_bg_list[Math.floor(Math.random() * color_bd_bg_list.length)]
}

function plotCoauthor(data, canvas_id) {
    //var number_test = data[1][0][0].split(" ").slice(data[1][0][0].split(" ").length - 1);
    //var number = number_test[0].split("").slice(1).slice("", number_test[0].split("").length - 2).join("");
    //var name = data[1][0][0].split(" ").slice(0, data[1][0][0].split(" ").length - 1).join(" ");
    var lengthOfAuthor = data[1].length;
    var authorDot = [];
    for (var i = 0; i < lengthOfAuthor; i++) {
        var pre_number = data[1][i][0].split(" ").slice(data[1][i][0].split(" ").length - 1);
        var numOfCoauthor = pre_number[0].split("").slice(1).slice("", pre_number[0].split("").length - 2).join("");
        var nameOfAuthor = data[1][i][0].split(" ").slice(0, data[1][i][0].split(" ").length - 1).join(" ");
        var int_numOfCoauthor = parseInt(numOfCoauthor);
        /*
         if (int_numOfCoauthor > 200) {
         int_numOfCoauthor /= 5;//40
         } else if (int_numOfCoauthor < 200 && int_numOfCoauthor > 150) {
         int_numOfCoauthor /= 5.2//38 28.84
         } else if (int_numOfCoauthor < 150 && int_numOfCoauthor > 100) {
         int_numOfCoauthor /= 4;//37.25  25
         } else if (int_numOfCoauthor < 100 && int_numOfCoauthor > 50) {
         int_numOfCoauthor /= 2.8;//35.35 17.5
         }
         */
        var _x = Math.floor(Math.random() * 900);
        var _y = Math.floor(Math.random() * 450);
        var _bgbdColor = bg_bd_color();
        authorDot.push({
            label: nameOfAuthor,
            backgroundColor: _bgbdColor["backgroundColor"],
            borderColor: _bgbdColor["borderColor"],
            data: [{
                x: _x,
                y: _y,
                r: int_numOfCoauthor
            }]
        })
    }

    var ctx = document.getElementById("bubble-chart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bubble',
        data: {
            labels: "Africa",
            datasets: authorDot
        },
        options: {
            legend: {
                display: false
            },
            title: {
                display: false,
                text: 'Predicted world population (millions) in 2050'
            }, scales: {
                yAxes: [{
                    display: false,
                    scaleLabel: {
                        display: false,
                        labelString: ""
                    },
                    ticks: {
                        beginAtZero: true
                    },
                    gridLines: {
                        display: false,
                        drawBorder: false
                    }
                }],
                xAxes: [{
                    display: false,
                    scaleLabel: {
                        display: false,
                        labelString: ""
                    },
                    ticks: {
                        beginAtZero: true
                    },
                    gridLines: {
                        display: false,
                        drawBorder: false
                    }
                }]
            }
        }
    });


}