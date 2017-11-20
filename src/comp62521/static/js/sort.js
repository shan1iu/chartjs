function sort(table) {
    // get the headers of the table
    var headers = table.getElementsByTagName("th");
    for (var i = 0; i < headers.length; i++) {
        (function (n) {
            var flag = true;
            headers[n].onclick = function () {
                var tbody = table.tBodies[0];
                var rows = tbody.getElementsByTagName("tr");
                rows = Array.prototype.slice.call(rows, 0);
                rows.sort(function (row1, row2) {
                    var cell1 = row1.getElementsByTagName("td")[n];
                    var cell2 = row2.getElementsByTagName("td")[n];
                    var val1 = cell1.textContent || cell1.innerText;
                    var val2 = cell2.textContent || cell2.innerText;
                    // if it is a number then parse it into type number
                    val1 = checkByExactValue(val1);
                    val2 = checkByExactValue(val2);
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
/**
 *
 * @param val
 * @returns {*}
 * 1. if val is number, parse it into type number
 * 2. if val is string, get the last word
 *  2.1 if last word is a number then drop it
 *  2.2 if last word is "Jr."  then drop it
 */
function checkByExactValue(val) {
    if (!isNaN(parseInt(val))) {
        val = parseInt(val)
    } else {
        var val_list = val.split(" ");
        val = val_list[val_list.length - 1];
        if (!isNaN(parseInt(val)) || val === "Jr.") {
            val = val_list[val_list.length - 2];
        }
        val = val.toLowerCase();
    }
    return val
}

window.onload = function () {
    var table = document.getElementsByTagName("table");
    for (var i = 0; i < table.length; i++) {
        sort(table[i])
    }
};
