function dropWhitespace(name) {
    var name_list = name.split(" ");
    var result = "";
    for (var i = 0; i < name_list.length; i++) {
        result += name_list[i];
    }
    return result;
}

function parseData(data) {
    var author1 = data[0][0];
    var b = data[0].length - 1;
    var author2 = data[0][b];
    /*
     data = [
     ["Author C", "Author G", "Author A", "Author E"],
     ["Author C", "Author B", "Author X", "Author E"],
     ["Author C", "Author B", "Author Y", "Author E"]
     ];
     data[i] = ["Author C", "Author G", "Author A", "Author E"]
     data[i][j] = "Author C"
     */

    var result_nodes = [];
    var result_edges = [];

    result_nodes.push({data: {id: dropWhitespace(author1), name: author1}});
    result_nodes.push({data: {id: dropWhitespace(author2), name: author2}});

    // add nodes

    for (var i = 0; i < data.length; i++) {
        for (var j = 0; j < data[0].length; j++) {
            var flag1 = true;
            for (var k = 0; k < result_nodes.length; k++) {
                if (result_nodes[k]["data"]["id"] === dropWhitespace(data[i][j])) {
                    flag1 = false;
                    break;
                }
            }
            if (flag1) {
                result_nodes.push({data: {id: dropWhitespace(data[i][j]), name: data[i][j]}});
            }
        }
    }

    //add edges
    for (var ii = 0; ii < data.length; ii++) {
        for (var jj = 0; jj < data[0].length; jj++) {
            if (result_edges.length === 0) {
                result_edges.push({
                    data: {
                        source: dropWhitespace(data[ii][jj]),
                        target: dropWhitespace(data[ii][jj + 1])
                    }
                });
            } else {

                if (jj !== data[0].length - 1) {
                    var flag2 = true;
                    for (var kk = 0; kk < result_edges.length; kk++) {
                        if (result_edges[kk]["data"]["source"] === dropWhitespace(data[ii][jj]) && result_edges[kk]["data"]["target"] === dropWhitespace(data[ii][jj + 1])) {
                            flag2 = false;
                            break;
                        }
                    }
                    if (flag2) {
                        result_edges.push({
                            data: {
                                source: dropWhitespace(data[ii][jj]),
                                target: dropWhitespace(data[ii][jj + 1])
                            }
                        });
                    }
                }
            }
        }
    }
    return [result_nodes, result_edges];
}

function template(id, arg_node, arg_edge) {
    return {
        container: document.getElementById(id),
        boxSelectionEnabled: false,
        autounselectify: true,
        userZoomingEnabled: false,
        layout: {
            name: 'dagre'
        },
        style: [
            {
                selector: 'node',
                style: {
                    'content': 'data(name)',
                    'text-valign': 'center',
                    'color': 'white',
                    'text-outline-width': 2,
                    'text-outline-color': '#999',
                    'background-color': '#999',
                    'padding': '20px'
                }
            },
            {
                selector: 'edge',
                style: {
                    'curve-style': 'segments',
                    'width': 2,
                    'target-arrow-shape': 'triangle',
                    'background-color': 'black',
                    'line-color': 'black',
                    'target-arrow-color': 'black',
                    'source-arrow-color': 'black',
                    'text-outline-color': 'black'
                }
            }
        ],
        elements: {
            nodes: arg_node,
            edges: arg_edge
        }
    };
}


// function parseDataBan(data) {
//     var result_nodes = [];
//     var result_edges = [];
//     for (var i = 0; i < data.length; i++) {
//         if (i === 0) { // if it is the first element.
//             var node_dict0 = {data: {id: ""}};
//             node_dict0["data"]["id"] = dropWhitespace(data[i]);
//             result_nodes.push(node_dict0);
//         } else { // if it is not the first element.
//             if (typeof data[i] === "string" && typeof data[i - 1] === "string") {
//                 /**
//                  * A -> B
//                  */
//                 var node_dict1 = {data: {id: ""}};
//                 var edge_dict1 = {data: {source: "", target: ""}};
//                 node_dict1["data"]["id"] = dropWhitespace(data[i]);
//                 edge_dict1["data"]["source"] = dropWhitespace(data[i - 1]);
//                 edge_dict1["data"]["target"] = dropWhitespace(data[i]);
//                 result_nodes.push(node_dict1);
//                 result_edges.push(edge_dict1);
//             } else if (typeof data[i] === "string" && typeof data[i - 1] === "object") {
//                 /**
//                  *  B
//                  *   \
//                  *    A
//                  *   /
//                  *  C
//                  */
//                 var node_dict2 = {data: {id: ""}};
//                 node_dict2["data"]["id"] = dropWhitespace(data[i]);
//                 result_nodes.push(node_dict2);
//                 var length2 = data[i - 1].length;
//                 for (var j = 0; j < length2; j++) {
//                     var edge_dict2 = {data: {source: "", target: ""}};
//                     edge_dict2["data"]["target"] = dropWhitespace(data[i]);
//                     edge_dict2["data"]["source"] = dropWhitespace(data[i - 1][j]);
//                     result_edges.push(edge_dict2);
//                 }
//             } else if (typeof data[i] === "object" && typeof data[i - 1] === "string") {
//                 /**
//                  *    B
//                  *   /
//                  *  A
//                  *   \
//                  *    C
//                  */
//                 var length3 = data[i].length;
//                 for (var k = 0; k < length3; k++) {
//                     var node_dict3 = {data: {id: ""}};
//                     node_dict3["data"]["id"] = dropWhitespace(data[i][k]);
//                     var edge_dict3 = {data: {source: "", target: ""}};
//                     edge_dict3["data"]["target"] = dropWhitespace(data[i][k]);
//                     edge_dict3["data"]["source"] = dropWhitespace(data[i - 1]);
//                     result_nodes.push(node_dict3);
//                     result_edges.push(edge_dict3);
//                 }
//             }
//         }
//     }
//     return [result_nodes, result_edges];
// }
