function sort(table) {
    // get the headers of the table
    var headers = table.getElementsByTagName("th");
    for (var i = 0; i < headers.length; i++) {
        (function (n) {
            var flag = true;
            headers[n].onclick = function () {
                console.log(flag);
                var tbody = table.tBodies[0];
                var rows = tbody.getElementsByTagName("tr");
                rows = Array.prototype.slice.call(rows, 0);
                rows.sort(function (row1, row2) {
                    var cell1 = row1.getElementsByTagName("td")[n];
                    var cell2 = row2.getElementsByTagName("td")[n];
                    var val1 = cell1.textContent || cell1.innerText;
                    var val2 = cell2.textContent || cell2.innerText;
                    if (!isNaN(parseInt(val1))) {
                        val1 = parseInt(val1)
                    }
                    if (!isNaN(parseInt(val2))) {
                        val2 = parseInt(val2)
                    }
                    if (val1 < val2) {
                        return -1;
                    } else if (val1 > val2) {
                        return 1;
                    } else {
                        return 0;
                    }
                });
                if (flag) {
                    rows.reverse();
                }
                for (var i = 0; i < rows.length; i++) {
                    tbody.appendChild(rows[i]);
                }
                flag = !flag;
            }
        })(i)
    }
}

window.onload = function () {
    var table = document.getElementsByTagName("table");
    for (var i = 0; i < table.length; i++) {
        sort(table[i])
    }
};
