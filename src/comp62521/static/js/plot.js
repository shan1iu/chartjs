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

function ajaxDataAverages(url) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            console.log(response["data"]);
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
    console.log(button_id, canvas_id);
    console.log($("#" + button_id).attr('disabled', 'disabled').parent().siblings().children().removeAttr('disabled'));
    $("#" + button_id).attr('disabled', 'disabled').parent().parent().siblings().children().children().removeAttr('disabled');
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

    var lengthOfCanvas = dataOfType.length * 10;
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
